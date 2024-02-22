import requests, time

TIMESTAMP = 1
CONTRACTS = {
    "XOXNO": "erd1qqqqqqqqqqqqqpgq6wegs2xkypfpync8mn2sa5cmpqjlvrhwz5nqgepyg8",
    "Frame IT": "erd1qqqqqqqqqqqqqpgq705fxpfrjne0tl3ece0rrspykq88mynn4kxs2cg43s",
}
url = "https://api.multiversx.com/transfers?size=10000&receiver=erd1qqqqqqqqqqqqqpgqmuzgkurn657afd3r2aldqy2snsknwvrhc77q3lj8l6"
for contract in CONTRACTS:
    url += f"&sender={CONTRACTS[contract]}"
url += f"&status=success&after={TIMESTAMP}"

response = requests.get(url).json()

data_nft_report = {}

i = 0
for transfer in response:
    original_hash = transfer["originalTxHash"]
    detailed_url = f"https://api.multiversx.com/transactions/{original_hash}"
    detailed_response = requests.get(detailed_url).json()
    operations = detailed_response["operations"]

    sft_transfer = [
        op
        for op in operations
        if op["type"] == "nft" and op["collection"] == "DATANFTFT-e936d4"
    ][0]
    sft_id = sft_transfer["identifier"]
    if sft_id not in data_nft_report:
        data_nft_report[sft_id] = {"EGLD": 0}

    transfer_to_mint_sc = [
        op
        for op in operations
        if op["receiver"]
        == "erd1qqqqqqqqqqqqqpgqmuzgkurn657afd3r2aldqy2snsknwvrhc77q3lj8l6"
    ][0]
    if transfer_to_mint_sc["type"] == "egld":
        data_nft_report[sft_id]["EGLD"] += int(transfer_to_mint_sc["value"]) / 10**18
    elif transfer_to_mint_sc["type"] == "esdt":
        if transfer_to_mint_sc["identifier"] not in data_nft_report[sft_id]:
            data_nft_report[sft_id][transfer_to_mint_sc["identifier"]] = 0
        data_nft_report[sft_id][transfer_to_mint_sc["identifier"]] += (
            int(transfer_to_mint_sc["value"]) / 10**18
        )

    time.sleep(1.83)
    print(i)
    i += 1
print(data_nft_report)
