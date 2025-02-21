import tkinter as tk
from tkinter import messagebox
import yaml

# Function to generate YAML
def generate_config():
    region = region_entry.get()
    app_name = app_name_entry.get()
    num_accounts = int(num_accounts_entry.get())
    
    accounts = {}
    for i in range(num_accounts):
        account_id = account_id_entries[i].get()
        security_group = security_group_entries[i].get()
        subnet_ids = [x.strip() for x in subnet_id_entries[i].get().split(",")]
        vpc_id = vpc_id_entries[i].get()
        tf_bucket = tf_bucket_entries[i].get()
        tf_table = tf_table_entries[i].get()
        ssl_certificate_arn = ssl_certificate_arn_entries[i].get()
        route53_zone_id = route53_zone_id_entries[i].get()
        domain = domain_entries[i].get()
        cross_account_role = cross_account_role_entries[i].get()
        execution_role = execution_role_entries[i].get()
        task_role = task_role_entries[i].get()

        accounts[account_id] = {
            "security_group": security_group,
            "subnet_ids": subnet_ids,
            "vpc_id": vpc_id,
            "tf_bucket": tf_bucket,
            "tf_table": tf_table,
            "ssl_certificate_arn": ssl_certificate_arn,
            "route53_zone_id": route53_zone_id,
            "domain": domain,
            "cross_account_role": cross_account_role,
            "execution_role": execution_role,
            "task_role": task_role
        }

    config = {
        "region": region,
        "app_name": app_name,
        "aws_accounts": accounts
    }

    with open("config.yaml", "w") as f:
        yaml.dump(config, f)

    messagebox.showinfo("Success", "config.yaml file generated!")

# Creating the main window
root = tk.Tk()
root.title("Config Generator")

# Entry widgets for user input
tk.Label(root, text="Enter the region: ").grid(row=0, column=0)
region_entry = tk.Entry(root)
region_entry.grid(row=0, column=1)

tk.Label(root, text="Enter the app name: ").grid(row=1, column=0)
app_name_entry = tk.Entry(root)
app_name_entry.grid(row=1, column=1)

tk.Label(root, text="Enter the number of accounts: ").grid(row=2, column=0)
num_accounts_entry = tk.Entry(root)
num_accounts_entry.grid(row=2, column=1)

# Creating placeholders for account input
account_id_entries = []
security_group_entries = []
subnet_id_entries = []
vpc_id_entries = []
tf_bucket_entries = []
tf_table_entries = []
ssl_certificate_arn_entries = []
route53_zone_id_entries = []
domain_entries = []
cross_account_role_entries = []
execution_role_entries = []
task_role_entries = []

def create_account_entries():
    num_accounts = int(num_accounts_entry.get())
    for i in range(num_accounts):
        row = 4 + i * 13
        tk.Label(root, text=f"Enter info for account {i + 1}: ").grid(row=row, column=0, columnspan=2)
        
        tk.Label(root, text="Account ID: ").grid(row=row+1, column=0)
        account_id_entry = tk.Entry(root)
        account_id_entry.grid(row=row+1, column=1)
        account_id_entries.append(account_id_entry)
        
        tk.Label(root, text="Security Group: ").grid(row=row+2, column=0)
        security_group_entry = tk.Entry(root)
        security_group_entry.grid(row=row+2, column=1)
        security_group_entries.append(security_group_entry)
        
        tk.Label(root, text="Subnet IDs: ").grid(row=row+3, column=0)
        subnet_id_entry = tk.Entry(root)
        subnet_id_entry.grid(row=row+3, column=1)
        subnet_id_entries.append(subnet_id_entry)
        
        tk.Label(root, text="VPC ID: ").grid(row=row+4, column=0)
        vpc_id_entry = tk.Entry(root)
        vpc_id_entry.grid(row=row+4, column=1)
        vpc_id_entries.append(vpc_id_entry)
        
        tk.Label(root, text="TF Bucket: ").grid(row=row+5, column=0)
        tf_bucket_entry = tk.Entry(root)
        tf_bucket_entry.grid(row=row+5, column=1)
        tf_bucket_entries.append(tf_bucket_entry)
        
        tk.Label(root, text="TF Table: ").grid(row=row+6, column=0)
        tf_table_entry = tk.Entry(root)
        tf_table_entry.grid(row=row+6, column=1)
        tf_table_entries.append(tf_table_entry)
        
        tk.Label(root, text="SSL Certificate ARN: ").grid(row=row+7, column=0)
        ssl_certificate_arn_entry = tk.Entry(root)
        ssl_certificate_arn_entry.grid(row=row+7, column=1)
        ssl_certificate_arn_entries.append(ssl_certificate_arn_entry)
        
        tk.Label(root, text="Route53 Zone ID: ").grid(row=row+8, column=0)
        route53_zone_id_entry = tk.Entry(root)
        route53_zone_id_entry.grid(row=row+8, column=1)
        route53_zone_id_entries.append(route53_zone_id_entry)
        
        tk.Label(root, text="Domain: ").grid(row=row+9, column=0)
        domain_entry = tk.Entry(root)
        domain_entry.grid(row=row+9, column=1)
        domain_entries.append(domain_entry)
        
        tk.Label(root, text="Cross Account Role: ").grid(row=row+10, column=0)
        cross_account_role_entry = tk.Entry(root)
        cross_account_role_entry.grid(row=row+10, column=1)
        cross_account_role_entries.append(cross_account_role_entry)
        
        tk.Label(root, text="Execution Role: ").grid(row=row+11, column=0)
        execution_role_entry = tk.Entry(root)
        execution_role_entry.grid(row=row+11, column=1)
        execution_role_entries.append(execution_role_entry)
        
        tk.Label(root, text="Task Role: ").grid(row=row+12, column=0)
        task_role_entry = tk.Entry(root)
        task_role_entry.grid(row=row+12, column=1)
        task_role_entries.append(task_role_entry)

# Button to create the account entries based on user input
tk.Button(root, text="Generate Config", command=create_account_entries).grid(row=5, column=1, rowspan=3)

# Button to generate the config file
tk.Button(root, text="Generate YAML", command=generate_config).grid(row=100, column=0, columnspan=2)

root.mainloop()
