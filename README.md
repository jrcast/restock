# RESTock

## What is RESTock?

RESTock is a simple tool based on python3 used to obtain the stock price data from www.alphavantage.co/


## Getting started

The easiest way to run RESTock is to pull the public docker image

```
docker pull jrcast/restock
```

Or can build your own by pulling this git repository and running the following:
```
docker build -t restock -f Dockerfile .
```

### Running RESTock

To run RESTock locally:

```
docker run -ti --rm  -e APIKEY=[YOUR_APIKEY] -e SYMBOL=AAPL -e NDAYS=5 -p 10000:10000 restock
```

To deploy to Kubernetes: 

```
kubectl create secret generic apikey --from-literal=apikey=[YOUR_APIKEY]
kubectl create -f k8s
```

### Requesting data from RESTock

Once your container or pod is running, you can get market data by sending GET requests. Note that RESTock uses port 10000 by default. Currently, RESTock only support two parameters:

| Parameter | Type  | Example |
|--------|--------|--------|
| symbol| str | AAPL |
| ndays | int | 4 |

You can skip the request parameters and specify a default symbol and ndays by setting the SYMBOL and NDAYS environmental variables in the container.

Sample request:
`http://localhost:10000?symbol=aapl&ndays=2`

## Docker

Releases are automatically built and published to dockerhub: jrcast/restock


## Current limitations:

1. Returned data is currently limited to the daily close price of the specified stock symbol.
