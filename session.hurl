# session.hurl

# ============================================
# GET /
# ============================================
GET {{host}}/
HTTP/1.1 200
[Asserts]
jsonpath "$.status" == "ok"

# ============================================
# GET /health
# ============================================
GET {{host}}/health
HTTP/1.1 200
[Asserts]
jsonpath "$.service" == "running"

# ============================================
# GET /clients
# ============================================
GET {{host}}/clients
HTTP/1.1 200
[Asserts]
jsonpath "$[0].id" exists
jsonpath "$[0].name" exists

# ============================================
# GET /clients/1
# ============================================
GET {{host}}/clients/1
HTTP/1.1 200
[Asserts]
jsonpath "$.id" == 1
jsonpath "$.name" exists

# ============================================
# POST /clients
# ============================================
POST {{host}}/clients
Content-Type: application/json

{
  "id": 2,
  "name": "John Doe",
  "email": "john@example.com"
}
HTTP/1.1 201
[Asserts]
jsonpath "$.id" == 2
jsonpath "$.name" == "John Doe"
jsonpath "$.email" == "john@example.com"

# ============================================
# GET /clients/2
# ============================================
GET {{host}}/clients/2
HTTP/1.1 200
[Asserts]
jsonpath "$.id" == 2
jsonpath "$.name" == "John Doe"

# ============================================
# PUT /clients/2
# ============================================
PUT {{host}}/clients/2
Content-Type: application/json

{
  "id": 2,
  "name": "John Smith",
  "email": "johnsmith@example.com"
}
HTTP/1.1 200
[Asserts]
jsonpath "$.id" == 2
jsonpath "$.name" == "John Smith"

# ============================================
# GET /clients/2 after update
# ============================================
GET {{host}}/clients/2
HTTP/1.1 200
[Asserts]
jsonpath "$.name" == "John Smith"

# ============================================
# POST /purchase
# ============================================
POST {{host}}/purchase
Content-Type: application/json

{
  "clientId": 2,
  "amount": 200,
  "currency": "USD",
  "purchaseDate": "2025-09-29",
  "purchaseCountry": "USA"
}
HTTP/1.1 200
[Asserts]
jsonpath "$.status" == "Approved"
jsonpath "$.purchase.clientId" == 2
jsonpath "$.purchase.originalAmount" == 200.0
jsonpath "$.purchase.discountApplied" == 30.0
jsonpath "$.purchase.finalAmount" == 170.0
jsonpath "$.purchase.benefit" contains "15% descuento"
