import yaml
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Input, Pretty, TextArea
from textual.containers import VerticalScroll
from textual.validation import Number
from textual.screen import Screen




class QuotedStringDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(QuotedStringDumper, self).increase_indent(flow, indentless)

    def write_scalar(self, tag, value, style=None):
        # Always quote strings
        return super(QuotedStringDumper, self).write_scalar(tag, value, style='"')

class ConfirmationScreen(Screen):
    CSS_PATH = "styles.tcss"
        
    def compose(self) -> ComposeResult:
        yield Label("Config Yaml Generated", id="confirmation_label")
        yield Button("Exit", id="exit_button")
        
    def _on_mount(self):
        self.screen.styles.background = "darkblue"
        self.screen.styles.border = ("heavy", "black")
        self.set_interval(0.1, self.update_input_styles)
        
    def update_input_styles(self) -> None:
        for input_widget in self.query(Label):
            input_widget.styles._align_height = "center" 
            input_widget.styles._align_width = "center"      
             
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit_button":
            self.app.exit()

class AccountScreen(Screen):
    def _on_mount(self):
        self.screen.styles.background = "darkblue"
        self.screen.styles.border = ("heavy", "black")
    def compose(self) -> ComposeResult:
        """Create the widgets for account input."""
        self.account_inputs = []
        for i in range(self.app.num_accounts):
            yield Label(f"Account {i+1} Details:", id=f"account_details_{i}")
            self.account_inputs.append(
                {
                    'account_id': Input(placeholder=f"Account ID"),
                    'security_group': Input(placeholder=f"Security Group", value="sg-"),
                    'subnet_ids': TextArea(
                        soft_wrap=True,
                        show_line_numbers=True,
                        line_number_start=1,
                        theme="vscode_dark",
                        id=f"subnet_ids_{i}",
                        text="subnet-\nsubnet-"
                    ),
                    'vpc_id': Input(placeholder=f"VPC ID", value="vpc-"),
                    'tf_bucket': Input(placeholder=f"Terraform Bucket"),
                    'tf_table': Input(placeholder=f"Terraform Table"),
                    'ssl_certificate_arn': Input(placeholder=f"SSL Certificate ARN", value=f"arn:aws:acm:{self.app.region}:"),
                    'route53_zone_id': Input(placeholder=f"Route53 Zone ID"),
                    'domain': Input(placeholder=f"Domain"),
                    'cross_account_role': Input(placeholder=f"Cross Account Role"),
                    'execution_role': Input(placeholder=f"Execution Role"),
                    'task_role': Input(placeholder=f"Task Role"),
                }
            )
        
        # Yield each input for the current account
        # for field in self.account_inputs[i].values():
        #     yield Label(f"{field.placeholder}")  # Label for each input
        #     yield field  # The input field
        # self.account_inputs = []
        # for i in range(self.app.num_accounts):
        #     yield Label(f"Account {i+1} Details:")
        #     self.account_inputs.append({
        #         "account_id": Input(placeholder=f"Account ID"),
        #         "security_group": Input(placeholder=f"Security Group"),
        #         "subnet_ids": Input(placeholder=f"Subnet IDs"),
        #         "vpc_id": Input(placeholder=f"VPC ID"),
        #         "tf_bucket": Input(placeholder=f"Terraform Bucket"),
        #         "tf_table": Input(placeholder=f"Terraform Table"),
        #         "ssl_certificate_arn": Input(placeholder="SSL Certificate ARN", value=f"arn:aws:acm:{self.app.region}:"),
        #         "route53_zone_id": Input(placeholder=f"Route53 Zone ID"),
        #         "domain": Input(placeholder=f"Domain"),
        #         "cross_account_role": Input(placeholder=f"Cross Account Role"),
        #         "execution_role": Input(placeholder=f"Execution Role"),
        #         "task_role": Input(placeholder=f"Task Role")
        #     })
            
            # Yield each input for the current account
            yield Label("Account ID")  # Label for each input
            yield self.account_inputs[i]["account_id"]
            yield Label("Security Group")  # Label for each input
            yield self.account_inputs[i]["security_group"]
            yield Label("Subnet IDs")  # Label for each input
            yield self.account_inputs[i]["subnet_ids"]
            yield Label("VPC ID")  # Label for each input
            yield self.account_inputs[i]["vpc_id"]
            yield Label("Terraform Bucket")  # Label for each input   
            yield self.account_inputs[i]["tf_bucket"]
            yield Label("Terraform Table")  # Label for each input  
            yield self.account_inputs[i]["tf_table"]
            yield Label("SSL Certificate ARN")  # Label for each input
            yield self.account_inputs[i]["ssl_certificate_arn"]
            yield Label("Route53 Zone ID")  # Label for each input
            yield self.account_inputs[i]["route53_zone_id"]
            yield Label("Domain")  # Label for each input
            yield self.account_inputs[i]["domain"]
            yield Label("Cross Account Role")            
            yield self.account_inputs[i]["cross_account_role"]
            yield Label("Execution Role")            
            yield self.account_inputs[i]["execution_role"]
            yield Label("Task Role")            
            yield self.account_inputs[i]["task_role"]

        # Add the Save button
        yield Button("Generate Yaml", id="save")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle saving the account data."""
        account_data = {
            'region': self.app.region,
            'app_name': self.app.app_name,
            'aws_accounts': {}
        }
        for account_input in self.account_inputs:
            account_id = account_input["account_id"].value  # Use account_id as key
            account_info = {
                "security_group": account_input["security_group"].value,
                "subnet_ids": account_input["subnet_ids"].text.split("\n"),
                "vpc_id": account_input["vpc_id"].value,
                "tf_bucket": account_input["tf_bucket"].value,
                "tf_table": account_input["tf_table"].value,
                "ssl_certificate_arn": account_input["ssl_certificate_arn"].value,
                "route53_zone_id": account_input["route53_zone_id"].value,
                "domain": account_input["domain"].value,
                "cross_account_role": account_input["cross_account_role"].value,
                "execution_role": account_input["execution_role"].value,
                "task_role": account_input["task_role"].value
            }
            account_data["aws_accounts"][account_id] = account_info

        with open('config.yaml', 'w') as file:
            yaml.dump(account_data, file, default_flow_style=False, Dumper=QuotedStringDumper)
        with open('fetch_jobs/config.yaml', 'w') as file:
            yaml.dump(account_data, file, default_flow_style=False)
        

class MyApp(App):
    CSS_PATH = "styles.tcss"
    def compose(self) -> ComposeResult:
        yield Label("Please Enter Your Region:")
        yield Input(value=f"us-east-1", id="region")
        yield Label("Please Enter Your App Name:")
        yield Input(value=f"myapp", id="app_name")
        yield Label("Please Enter Number of Accounts:")
        yield Input(value=f"1", id="no_accounts", validators=[Number(minimum=1, maximum=10)])
        yield Button("Next", id="next_button")
        yield Pretty([])

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Only show validation reasons for the number of accounts input
        if event.input.id == "no_accounts":
            if not event.validation_result.is_valid:
                self.query_one(Pretty).update(event.validation_result.failure_descriptions)
            else:
                self.query_one(Pretty).update([])

    async def on_mount(self) -> None:
        """Called when the widget is fully rendered."""
        self.screen.styles.background = "darkblue"
        self.screen.styles.border = ("heavy", "black")
        self.region_input = self.query_one("#region", Input)
        self.app_name_input = self.query_one("#app_name", Input)
        self.num_accounts_input = self.query_one("#no_accounts", Input)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the button click event."""
        # Access the input value after widget rendering
        region = self.region_input.value
        app_name = self.app_name_input.value
        num_accounts = int(self.num_accounts_input.value)

        # Set app attributes
        self.region = region
        self.app_name = app_name
        self.num_accounts = num_accounts

        # Move to the next screen
        account_screen = AccountScreen()
        self.app.push_screen(account_screen)
        if event.button.id == "save":
            self.app.pop_screen()
            confirmation_screen = ConfirmationScreen()
            self.app.push_screen(confirmation_screen)

def main():
    app = MyApp()
    app.run()

if __name__ == "__main__":
    app = MyApp()
    app.run()