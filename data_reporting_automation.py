import psycopg2 as pg
from sshtunnel import SSHTunnelForwarder
import pandas as pd
import os
from datetime import date
import datetime
import json
import time
import requests
import msal

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def establish_ssh_tunnel(ssh_config, psql_config):
    print('Connecting to the PostgreSQL Database...')

    ssh_tunnel = SSHTunnelForwarder(
        ssh_config['host'],
        ssh_username=ssh_config['ssh_user'],
        ssh_private_key=ssh_config['ssh_pkey'],
        remote_bind_address=(psql_config['p_host'], psql_config['p_port']),
    )
    ssh_tunnel.start()

    conn = pg.connect(
        host="127.0.0.1",
        port=ssh_tunnel.local_bind_port,
        user=psql_config['psql_user'],
        password=psql_config['psql_pass'],
        database=psql_config['db']
    )
    
    print('Connected')
    return conn, ssh_tunnel

def execute_sql_query(conn, query):
    print('Fetching Records...')
    db_cursor = conn.cursor()
    db_cursor.execute(query)
    records = db_cursor.fetchall()
    cols = [x[0] for x in db_cursor.description]
    df = pd.DataFrame(records, columns=cols)
    print('Done...')
    return df

def save_data_to_excel(df, start_date, end_date, project_id):
    today = date.today()
    file_name = f"report_name_-{start_date}-to-{end_date}.xlsx"
    volume_dir = f'/path/to/{project_id}_LOCAL/volume_{today}/'
    parent_dir = f'/path/to/{project_id}_LOCAL/{today}/'
    
    if not os.path.exists(volume_dir):
        os.makedirs(volume_dir)
    
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    
    file_to_save = parent_dir + file_name
    df.to_excel(file_to_save, index=False)

def mount_veracrypt_drive(volume_path, password):
    print('Mounting drive...')
    try:
        os.system(f'veracrypt -f -t -k "" --pim=0 --protect-hidden=no --password="{password}" {volume_path}/{Project_ID}.dat /media/veracrypt1')
    except Exception as error:
        print("Mount Error:", error)
    
def copy_to_veracrypt_drive(source_file, mounted_drive):
    print('Writing files to mounted dir')
    try:
        os.system(f'cp {source_file} /media/veracrypt1/')
    except Exception as error:
        print('Copy error:', error)
        os.system('veracrypt -f -d /media/veracrypt1')

def dismount_veracrypt_drive():
    print('Dismounting drive....')
    try:
        os.system("veracrypt -f -d /media/veracrypt1")
    except Exception as error:
        print('Dismount error:', error)

def move_veracrypt_volume_to_directory(project_id, volume_dir):
    os.system(f'cp /path/to/{project_id}_LOCAL/{project_id}.dat {volume_dir}/{project_id}_report_{today}.dat')

def authenticate_and_upload_to_onedrive(onedrive_creds, project_id, volume_dir):
    CLIENT_ID = onedrive_creds['CLIENT_ID']
    TENANT_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    AUTHORITY_URL = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
    RESOURCE_URL = 'https://graph.microsoft.com/'
    API_VERSION = 'v1.0'
    SCOPES = ['Sites.ReadWrite.All', 'Files.ReadWrite.All']
    data_reporting_secret_id = onedrive_creds['secret_id']
    USERNAME = onedrive_creds['USERNAME']
    PASSWORD = onedrive_creds['PASSWORD']
    CLIENT_SECRET = onedrive_creds['CLIENT_SECRET']

    cognos_to_onedrive = msal.ClientApplication(CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY_URL)
    token = cognos_to_onedrive.acquire_token_by_username_password(USERNAME, PASSWORD, SCOPES)
    headers = {'Authorization': 'Bearer {}'.format(token['access_token'])}
    onedrive_destination = '{}/{}/me/drive/root:/Data Sharing/{}'.format(RESOURCE_URL, API_VERSION, project_id)
    
    for root, dirs, files in os.walk(volume_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.stat(file_path).st_size
            file_data = open(file_path, 'rb')
            
            if file_size < 4100000:
                print('Less than 4MB')
                r = requests.put(onedrive_destination + "/" + file_name + ":/content", data=file_data, headers=headers)
            else:
                upload_session = requests.post(onedrive_destination + "/" + file_name + ":/createUploadSession", headers=headers).json()
                
                with open(file_path, 'rb') as f:
                    total_file_size = os.path.getsize(file_path)
                    chunk_size = 327680
                    chunk_number = total_file_size // chunk_size
                    chunk_leftover = total_file_size - chunk_size * chunk_number
                    i = 0
                    while True:
                        chunk_data = f.read(chunk_size)
                        start_index = i * chunk_size
                        end_index = start_index + chunk_size
                        if not chunk_data:
                            break
                        if i == chunk_number:
                            end_index = start_index + chunk_leftover
                        headers = {'Content-Length': '{}'.format(chunk_size), 'Content-Range': 'bytes {}-{}/{}'.format(start_index, end_index-1, total_file_size)}
                        chunk_data_upload = requests.put(upload_session['uploadUrl'], data=chunk_data, headers=headers)
                        print(chunk_data_upload)
                        print(chunk_data_upload.json())
                        i = i + 1
            file_data.close()

if __name__ == '__main__':
    # Load credentials
    postgres_creds = read_json('/path/to/postgres_creds.json')
    onedrive_creds = read_json('/path/to/onedrive_creds.json')

    psql_config = {
        'p_host': postgres_creds['p_host'],
        'p_port': postgres_creds['p_port'],
        'db': postgres_creds['db'],
        'ssh': postgres_creds['ssh'],
        'ssh_user': postgres_creds['ssh_user'],
        'ssh_host': postgres_creds['ssh_host'],
        'ssh_pkey': postgres_creds['ssh_pkey'],
        'psql_user': postgres_creds['psql_user'],
        'psql_pass': postgres_creds['psql_pass']
    }

    Project_ID = 'Project1'

    # Set date ranges
    today = date.today()
    start_date_delta = datetime.timedelta(7)
    end_date_delta = datetime.timedelta(1)
    start_date = today - start_date_delta
    end_date = today - end_date_delta

    # Connect to the PostgreSQL database using an SSH tunnel
    conn, ssh_tunnel = establish_ssh_tunnel(psql_config, postgres_creds)
    
    # Read SQL query from a file and execute it
    sql_query = open('/path/to/' + Project_ID + '_daily.sql', 'r').read()
    df = execute_sql_query(conn, sql_query)
    
    # Save data to an Excel file
    save_data_to_excel(df, start_date, end_date, Project_ID)
    
    # Mount the VeraCrypt drive
    veracrypt_password = open('/path/to/' + Project_ID + '_LOCAL/' + Project_ID + '_pass.txt').read().strip()
    mount_veracrypt_drive('/path/to', veracrypt_password)
    
    # Copy the Excel file to the mounted VeraCrypt drive
    copy_to_veracrypt_drive(file_to_save, '/media/veracrypt1')
    
    # Dismount the VeraCrypt drive
    dismount_veracrypt_drive()
    
    # Move the VeraCrypt volume to a directory
    move_veracrypt_volume_to_directory(Project_ID, volume_dir)
    
    # Authenticate and upload to OneDrive
    authenticate_and_upload_to_onedrive(onedrive_creds, Project_ID, volume_dir)
