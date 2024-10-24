import requests
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

# https://ca-central-1.console.aws.amazon.com/elasticbeanstalk/home?region=ca-central-1#/environment/dashboard?environmentId=e-akttpetemi
# http://ece444-pra5-try2.ca-central-1.elasticbeanstalk.com/ 

# sends the test cases to the api, and records the result & the latency. 
def api_call(url, test):
    start = time.time()
    result = requests.post(url, test)
    end = time.time()

    latency = end - start 
    return result.status_code, latency 

def boxplot():
    df = pd.read_csv("test_results.csv")

    plt.figure(figsize=(10, 6))
    df.boxplot(column="Latency (s)", by="Test Nr", grid=False)

    plt.title("Latency by Test Nr")
    plt.suptitle("")
    plt.xlabel("Test Nr")
    plt.ylabel("Latency (s)")

    plt.savefig("latency_boxplot.png")
    print("Boxplot saved to 'latency_boxplot.png'.")

    # Show the plot
    plt.show()
    return

def test():
    url = "http://ece444-pra5-try2.ca-central-1.elasticbeanstalk.com/"

    test_text = ["Donald Trump won the 2024 Election",  # False
                "Toronto is the Capital of Ontario",    # True 
                "The USSR exists today",                # False 
                "Christmas is celebrated in december"]  # True
    test_results = []

    print("starting api calls")
    for i in range(100):
        for num, text in enumerate(test_text):
            print(num, text)
            status_code, latency = api_call(url, text)
            test_results.append([num, text, latency])
    
    print("finished api calls")
    print("starting writing results to csv")
    with open("test_results.csv", "w", newline='') as f: 
        writer = csv.writer(f)
        writer.writerow(["Test Nr", "Article", "Latency (s)"])
        writer.writerows(test_results)
    print("finished writing results to csv") 
    boxplot()

    if __name__ == "__main__":
        test()