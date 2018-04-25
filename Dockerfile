FROM python:3.6

# Install dependencies for shapely
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y libgeos-c1 libgeos-dev \
 && rm -rf /var/lib/apt/lists/*

# Uncomment and set with valid connection string for use locally
#ENV TM_DB=postgresql://user:pass@host/db

WORKDIR /src

# Add and install Python modules
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose
EXPOSE 5000

# Gunicorn configured for single-core machine, if more cores available increase workers using formula ((cores x 2) + 1))
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "179", "manage:application"]
