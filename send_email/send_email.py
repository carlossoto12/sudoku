from azure.communication.email import EmailClient
from dotenv import load_dotenv
import os

class Send_email:

    def __init__(self, message, recipient, subject_line):
        self.message = message
        self.recipient = recipient
        self.subject_line = subject_line

    def send_the_email(self):
        response = False
        load_dotenv()
        try:
            connection_string = os.getenv("CONNECTION_STRING")
            client = EmailClient.from_connection_string(connection_string)

            message = {
                "senderAddress": os.getenv("SENDER_ADDRESS"),
                "recipients":  {
                    "to": [{"address": self.recipient }],
                },
                "content": {
                    "subject": self.subject_line,
                    "html": self.board_to_html(),
                }
            }

            poller = client.begin_send(message)
            result = poller.result()
            response = True

        except Exception as ex:
            print(ex)

        return response

    def board_to_html(self) -> str:
        board = self.message
        text = "<html><body style=\"color: red;\"><table>"
        for row in board:
            for i in range( len(row["columnas"]) ):
                text += "<tr>"
                for grid in row["columnas"]:
                    for value_in_row_of_grid in grid[i]:
                        text += f"<td>{value_in_row_of_grid}</td>"
                text += "</tr>"

        text += "</table></body></html>"
        return text