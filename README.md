# finview API

A simple API to fetch and analyze annual income statements for AAPL (Apple). The API is designed to provide insights into key metrics such as revenue, net income, gross profit, EPS(Earnings Per Share) and operating income. The API is built using Python and FastAPI framework.

## Deployment

* Try it out: https://finview-api.vercel.app
* API Documentation: https://finview-api.vercel.app/docs
* Alternative API Documentation: https://finview-api.vercel.app/redoc

## Getting started

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/sixtusagbo/finview-api
   cd finview-api
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Get a free API key from [Financial Modeling Prep](https://financialmodelingprep.com/)
5. Set your API key as an environment variable:
   ```bash
   export FMP_KEY=your_api_key_here  # On Windows use: set FMP_KEY=your_api_key_here
   ```

## Running the Project

To run the project locally:

```bash
fastapi dev api/v1/main.py
```

## Deployment

The API is deployed on Vercel and can be accessed at [https://finview-api.vercel.app/](https://finview-api.vercel.app/).

### API Documentation

- Interactive API documentation (Swagger UI): [https://finview-api.vercel.app/docs](https://finview-api.vercel.app/docs)
- OpenAPI specification: [https://finview-api.vercel.app/openapi.json](https://finview-api.vercel.app/openapi.json)
