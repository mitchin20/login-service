import os
import requests
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class TokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude root route
        exclude_path = ["/", "/login", "/verify-token", "/favicon.ico", "/docs", "/openapi.json"]
        if request.url.path in exclude_path:
            return await call_next(request)
        
        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            verify_token_url = os.getenv("VERIFY_TOKEN_URL", "http://127.0.0.1:8000")
            print(f"URL: {verify_token_url}")
            
            if not verify_token_url:
                raise HTTPException(status_code=500, detail="Verification token url is not set in the environment variables")

            # Call the login service to verify and possibly renew the token
            response = requests.post(
                f"{verify_token_url}/verify-token",
                json={"token": token}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            
            verified_token_data = response.json()
            new_token = verified_token_data["token"]

            # Pre-process the request - validate the token
            # Post-process the response - add new token to the response handers if the token was extended
            response_to_return = await call_next(request)
            if verified_token_data["extended"]:
                response_to_return.headers["Authorization"] = f"Bearer {new_token}"
                response_to_return.headers["Token-Renewed"] = "True"
            else:
                response_to_return.headers["Token-Renewed"] = "False"
            
            return response_to_return

        else:
            raise HTTPException(status_code=401, detail="Authorization token required")
