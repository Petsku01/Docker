import json
import datetime

# Simulate processing some data
def process_data():
    # Load the API data saved by the Bash script
    try:
        with open('logs/api.log', 'r') as f:
            api_data = f.read()
        print(f"Processing API data: {api_data.strip()}")
        
        # Create a sample JSON file
        data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"),
            "message": "Processed by Python script",
            "status": "success"
        }
        with open('data/output.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Created output.json with processed data")
    except Exception as e:
        print(f"Error during processing: {str(e)}")

if __name__ == "__main__":
    process_data()