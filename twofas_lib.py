import json
import qrcode
import os

class QRCode:
    def __init__(self, issuer="", secret="", account="", digits="6", period="30", algorithm="SHA1", tokenType="TOTP"):
        self.issuer = issuer                # Account issuer
        self.tokenType= tokenType           # TOTP or HOTP
        self.secret = secret                # Base32 encoded secret
        self.account = account              # Account email or username

        self.digits = digits                # Digit number (default 6)
        self.period = period                # Period in seconds (default 30)
        self.algorithm = algorithm          # Hash algorithm (SHA1, SHA256, SHA512) (default SHA1)
       
        self.label = f"{issuer}:{account}"  # Account name / Account issuer @ Account email or username
        self.otpauth = f"otpauth://{self.tokenType}/{self.label}?secret={self.secret}&issuer={self.issuer}&digits={self.digits}&period={self.period}&algorithm={self.algorithm}"
    
def generate_qr_codes(file_path,output_dir):

    # Load json file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Parse json file and generate QR codes for each service
    for service in data["services"]:
        # Generate QrCode object
        try:
            qr_code = QRCode(
                    secret=service["secret"],
                    issuer=service["otp"]["issuer"],
                    tokenType=service["otp"]["tokenType"],
                    digits=service["otp"]["digits"] if "digits" in service["otp"] else "6",
                    period=service["otp"]["period"] if "period" in service["otp"] else "",
                    algorithm=service["otp"]["algorithm"] if "algorithm" in service["otp"] else "SHA1",
                    account=service["otp"]["account"],
                    )
            
            # Generate QR code based on QrCode OTPAuth URL
            qr_img = qrcode.make(qr_code.otpauth)
            output_file = os.path.join(output_dir, f"{qr_code.issuer}.png")
            qr_img.save(output_file)

            print(f"QRCode {qr_code.label} saved as {output_file}")
            
        except KeyError:
            print(f"JSON file for {service['otp']['label']} is not properly formatted or a value is missing")
                 