import requests
import subprocess
import argparse
##############
def execute_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()

def run_command(full_cmd,log_file):
	full_cmd_str = " ".join(full_cmd)
	print("Running:\t" + full_cmd_str)
	out,err = execute_command(full_cmd)
	error_log = open(log_file,"w")
	error_log.writelines("%s " % full_cmd_str)
	error_log.write(err.decode("utf8"))
	error_log.write(out.decode("utf8"))
	error_log.close()
	return print(f"All Done!")
###################
###################################################
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--hostname',default=None, type=str, help="Emedgene hostname [*.emg.illumina.com]")
	parser.add_argument('--user_name',default=None, type=str, help="User Name")
	parser.add_argument('--password', default=None, type=str, help="Password")
	parser.add_argument('--csv_file', default=None, type=str, help="Emedgene CSV file for batch case upload")
	args, extras = parser.parse_known_args()
	###############################
	hostname = args.hostname
	user_name = args.user_name
	password = args.password
	###################################
	### STEP 1: Authenticate and generate Bearer token
	route_login_platform = f'https://{hostname}.emg.illumina.com/api/auth/v2/api_login/'
	payload = {"username": user_name, "password": password}
	response = requests.post(route_login_platform, json=payload)
	access_token = response.json().get('access_token')
	token_type = response.json().get('token_type')
	bearer_token = f'{token_type.capitalize()} {access_token}'
	print(bearer_token)


	csv_file = args.csv_file
	batch_creation_string = f"node batchCasesCreator.js create -h https://{hostname}.emg.illumina.com -c {csv_file}"


	batch_creation_arr = batch_creation_string.split(" ")
	batch_creation_arr.append("-t")
	batch_creation_arr.append(bearer_token)
	print(batch_creation_arr)
	run_command(batch_creation_arr,"batch_creation.v1.error.log")

	batch_creation_arr1 = batch_creation_string.split(" ")
	batch_creation_arr1.append("-t")
	bearer_token_simplified = bearer_token.strip("Bearer ")
	batch_creation_arr1.append(bearer_token_simplified)
	print(batch_creation_arr1)
	run_command(batch_creation_arr1,"batch_creation.v2.error.log")
if __name__ == "__main__":
    main()