import asyncio
import os
from dotenv import load_dotenv
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, LoginPassword

load_dotenv()

from queue_manager import enqueue_email


class Authenticator:
    def __call__(self, server, session, envelope, mechanism, auth_data):
        fail_nothandled = AuthResult(success=False, handled=False)
        if mechanism not in ("LOGIN", "PLAIN"):
            return fail_nothandled

        if not isinstance(auth_data, LoginPassword):
            return fail_nothandled

        expected_user = os.getenv("SMTP_USER")
        expected_pass = os.getenv("SMTP_PASS")

        if auth_data.login.decode('utf-8') == expected_user and auth_data.password.decode('utf-8') == expected_pass:
            return AuthResult(success=True)

        return AuthResult(success=False, handled=True)


class MessageHandler:
    async def handle_DATA(self, server, session, envelope):
        if not session.authenticated:
            return '530 Authentication required'

        email_data = {
            "mail_from": envelope.mail_from,
            "rcpt_to": envelope.rcpt_tos,
            "data": envelope.content.decode('utf-8', errors='replace')
        }

        # enqueue_email(email_data)
        print("---- Queued email:", envelope.mail_from, "->", envelope.rcpt_tos)
        return '250 Message accepted for delivery'


if __name__ == "__main__":
    port = int(os.getenv("SMTP_PORT"))
    
    handler = MessageHandler()
    controller = Controller(
        handler, 
        hostname="0.0.0.0", 
        port=port, 
        authenticator=Authenticator(), 
        auth_required=True,
        auth_require_tls=False
    )

    print("SMTP Server listening on", port)
    controller.start()
    
    try:
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print("Error in asyncio loop:", e)

    finally:
        controller.stop()
