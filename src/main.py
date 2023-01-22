from integrations.dydx import connect_to_dydx

if __name__ == "__main__":
    try:
        connect_to_dydx()
    except Exception as e:
        print(f"Error while connecting to dydx: {e}")