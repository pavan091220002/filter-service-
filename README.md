# filter-service-

**Setup instructions**
1. Clone the Repository:

git clone <repository_url>
cd filter-service

2. Install Dependencies:
Ensure you have Python 3.7+ installed. Then, install the required dependencies:

pip install -r requirements.txt

3. Run the Application:

uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

**Api Documentation:**
**Endpoints**
**1. Get Items**

URL: /api/items
Method: GET
Description: Retrieve a list of fashion items with optional filtering and sorting.
Query Parameters:
category (optional): Filter by category.
min_price (optional): Filter by minimum price.
max_price (optional): Filter by maximum price.
size (optional): Filter by size.
color (optional): Filter by color.
designer (optional): Filter by designer.
min_rating (optional): Filter by minimum rating.
sort_by (optional): Sort by price (ascending/descending) or rating (descending).
page (default: 1): Page number.
page_size (default: 12): Number of items per page.

**2. Get Item by ID**

URL: /api/items/{item_id}
Method: GET
Description: Retrieve a single fashion item by its ID.

**3. Get Categories**
URL: /api/categories
Method: GET
Description: Retrieve a list of fashion items filtered by category.
Query Parameters:
category (optional): Filter by category.
page (default: 1): Page number.
page_size (default: 12): Number of items per page.

**4. Get Sizes**
URL: /api/sizes
Method: GET
Description: Retrieve a list of fashion items filtered by size.
Query Parameters:
size (optional): Filter by size.
page (default: 1): Page number.
page_size (default: 12): Number of items per page.

**5. Get Colors**
URL: /api/colors
Method: GET
Description: Retrieve a list of fashion items filtered by color.
Query Parameters:
color (optional): Filter by color.
page (default: 1): Page number.
page_size (default: 12): Number of items per page.

**6. Get Designers**
URL: /api/designers
Method: GET
Description: Retrieve a list of fashion items filtered by designer.
Query Parameters:
designer (optional): Filter by designer.
page (default: 1): Page number.
page_size (default: 12): Number of items per page.



**Design Choices**

**1. Data Loading:**
The data is loaded from a JSON file (data_items.json) at startup. This approach ensures that the data is readily available and reduces the need for database queries.
**2. Filtering and Sorting:**
Filtering and sorting are handled in-memory using list comprehensions and sorting functions. This approach is efficient for the given dataset size and ensures quick response times.
**3. Pagination:**
Pagination is implemented to handle large datasets efficiently. It ensures that only a subset of the data is returned, reducing the load on the server and improving performance.
**4. Error Handling:**
Comprehensive error handling is implemented to catch and handle exceptions such as file not found, JSON decoding errors, and invalid query parameters.



**Assumptions**

**1. Data Format:**
It is assumed that the data in data_items.json is well-formed and adheres to the expected schema.
**2. Performance:**
The dataset is assumed to be small enough to fit into memory, allowing for in-memory filtering and sorting.
**3. Concurrency:**
The application is designed to handle concurrent requests efficiently, leveraging FastAPI's asynchronous capabilities.


**Potential Improvements**
**1. Database Integration:**
For larger datasets, integrating a database (e.g., PostgreSQL, MongoDB) would be beneficial. This would allow for more efficient querying and better scalability.
**2. Caching:**
Implementing caching mechanisms (e.g., Redis) could further improve performance by reducing the need to reprocess data for frequent queries.
**3. Advanced Filtering:**
Adding more advanced filtering options, such as filtering by multiple categories, sizes, or colors, could enhance the user experience.
**4. Authentication and Authorization:**
Implementing authentication and authorization mechanisms would ensure that only authorized users can access certain endpoints or perform specific actions.
**5. Logging and Monitoring:**
Adding logging and monitoring tools (e.g., ELK Stack, Prometheus) would help in tracking the application's performance and identifying potential issues.
**6. Documentation:**
Enhancing the API documentation with more detailed examples and use cases would make it easier for developers to understand and use the API.
