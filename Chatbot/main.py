from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI(title="Customer Support Chatbot")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Product database simulation
products = {
    "1001": {"name": "Wireless Headphones", "price": 99.99, "stock": 45},
    "1002": {"name": "Bluetooth Speaker", "price": 59.99, "stock": 32},
    "1003": {"name": "Smart Watch", "price": 199.99, "stock": 18}
}

# Order database simulation
orders = {
    "ORD5001": {"status": "shipped", "products": ["1001", "1003"], "total": 299.98},
    "ORD5002": {"status": "processing", "products": ["1002"], "total": 59.99}
}

def get_bot_response(user_message: str) -> str:
    user_message = user_message.lower().strip()
    
    # Greetings
    if any(word in user_message for word in ["hi", "hello", "hey"]):
        return "Hello! Welcome to TechGadgets customer support. How can I help you today?"
    
    # Farewells
    elif any(word in user_message for word in ["bye", "goodbye"]):
        return "Thank you for contacting TechGadgets support. Have a great day!"
    
    # Products
    elif any(word in user_message for word in ["product", "item", "catalog"]):
        product_list = "\n".join([f"{pid}: {details['name']} (${details['price']})" 
                                for pid, details in products.items()])
        return f"Our current products:\n{product_list}\n\nWhich product would you like to know more about?"
    
    # Product details
    elif any(pid in user_message for pid in products.keys()):
        for pid, details in products.items():
            if pid in user_message:
                return (f"Product {pid}: {details['name']}\n"
                       f"Price: ${details['price']}\n"
                       f"In stock: {details['stock']} units")
    
    # Order status
    elif any(word in user_message for word in ["order", "track", "status"]):
        if any(ord_id.lower() in user_message for ord_id in orders.keys()):
            for ord_id, details in orders.items():
                if ord_id.lower() in user_message:
                    return (f"Order {ord_id.upper()} status: {details['status'].capitalize()}\n"
                           f"Products: {', '.join([products[pid]['name'] for pid in details['products']])}\n"
                           f"Total: ${details['total']}")
        return "Please provide your order number to check the status."
    
    # Contact information
    elif any(word in user_message for word in ["contact", "email", "phone"]):
        return ("You can reach us at:\n"
                "Email: support@techgadgets.com\n"
                "Phone: 1-800-TECH-SUP\n"
                "Hours: Mon-Fri 9AM-6PM EST")
    
    # Returns
    elif any(word in user_message for word in ["return", "refund"]):
        return ("Our return policy:\n"
                "- 30-day money back guarantee\n"
                "- Items must be unopened and in original packaging\n"
                "Would you like to initiate a return?")
    
    # Help
    elif "help" in user_message:
        return ("I can help with:\n"
                "- Product information\n"
                "- Order status\n"
                "- Returns and refunds\n"
                "- Contact information\n"
                "What would you like to know?")
    
    # Default response
    else:
        return ("I'm sorry, I didn't understand that. I can help with:\n"
                "- Product information\n"
                "- Order status\n"
                "- Returns\n"
                "- Contact details\n"
                "Please try asking about one of these topics.")

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/get_response")
async def get_response(user_message: str = Form(...)):
    bot_response = get_bot_response(user_message)
    return {"bot_response": bot_response}