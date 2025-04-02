import requests

# IP Address
host = 'http://127.0.0.1:5000'  # Change me

# Value to set
value = 0x0F0F

try:
    response = requests.get(f'{host}/{value:04X}')
    response.raise_for_status()

    data = response.json()
    print("✅ Response:")
    print(f"- Binär:   {data['message']}")
    print(f"- Hex:     {data['hex']}")
    print(f"- Decimal: {data['dec']}")

except requests.RequestException as e:
    print(f"❌ Error:\n{e}")