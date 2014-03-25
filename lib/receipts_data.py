"""
Receipts template data.

#1. single item receipt, online
#2. single return receipt, store
#3. single return receipt. no image., phone
#4. multiple items receipt. absence of size or color
#5. multiple items return receipt.
#6. multiple items receipt, no image.
"""

receipt_data = [

    #1. single item receipt, online
    {
        "customer_name": "Shanfour Mstrtest",
        "auid": 251643191,
        "transaction_id": "autotest001",
        "order_type": "ONLINE",
        "order_timestamp": 1388100100,
        "amount_for_points": 60,
        "order_detail": [
            {
                "variation_id": 206609100,
                "description": "YOUNG & RECKLESS Bold Logo Mens T-Shirt",
                "image": "http://www.tillys.com/tillys/images/catalog/large/206609100.jpg",
                "color": "Black",
                "size": "Large",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            }
        ],
        "sub_total": 86.97,
        "discount": -30,
        "tax": 1.35,
        "total_price": 91.32,
        "payment": {
            "payment_type": "GIFTCARD",
            "amount": 300,
            "card_number": "4523321411452025"
        }
    },

    #2. single return receipt, store
    [
        {
            "customer_name": "Shanfour Mstrtest",
            "auid": 251643191,
            "transaction_id": "autotest002",
            "order_type": "STORE",
            "order_timestamp": 1388200200,
            "amount_for_points": 90,
            "order_detail": [
                {
                    "variation_id": 207527200,
                    "description": "RETROFIT Kenneth Mens Shirt",
                    "image": "http://www.tillys.com/tillys/images/catalog/large/207527200.jpg",
                    "color": "haha",
                    "size": "what",
                    "unit_price": 99,
                    "quantity": 2,
                    "discount": 0.5,
                    "amount": 197
                }
            ],
            "sub_total": 166.97,
            "discount": -31.5,
            "tax": 1.35,
            "total_price": 196.32,
            "shop_id": 14
        },
        {
            "customer_name": "Shanfour Mstrtest",
            "auid": 251643191,
            "transaction_id": "autotest002",
            "order_type": "STORE",
            "order_timestamp": 1388300300,
            "amount_for_points": -20,
            "order_detail": [
                {
                    "variation_id": 207527200,
                    "description": "RETROFIT Kenneth Mens Shirt",
                    "image": "http://www.tillys.com/tillys/images/catalog/large/207527200.jpg",
                    "color": "haha",
                    "size": "what",
                    "unit_price": 99,
                    "quantity": -1,
                    "discount": 0.5,
                    "amount": 99.3
                }
            ],
            "sub_total": 86.97,
            "discount": 30,
            "tax": 1.35,
            "total_price": 91.32,
            "shop_id": 14
        }
    ],

    #3. single return receipt. no image., phone
    [
        {
            "customer_name": "Shanfour Mstrtest",
            "auid": 251643191,
            "transaction_id": "autotest003",
            "order_type": "PHONE",
            "order_timestamp": 1388400400,
            "amount_for_points": 100,
            "order_detail": [
                {
                    "variation_id": 13110000001,
                    "description": "Store & single item Bracelet 1",
                    "color": "Purle",
                    "size": "Small",
                    "unit_price": 5.19,
                    "quantity": 1,
                    "discount": 0.5,
                    "amount": 4.69
                }
            ],
            "sub_total": 86.97,
            "discount": 3,
            "tax": 1.35,
            "total_price": 91.32,
            "payment": {
                "payment_type": "PAYPAL",
                "amount": 100
            }
        },
        {
            "customer_name": "Shanfour Mstrtest",
            "auid": 251643191,
            "transaction_id": "autotest003",
            "order_type": "PHONE",
            "order_timestamp": 1388500400,
            "order_detail": [
                {
                    "variation_id": 13110000001,
                    "description": "Store & single item Bracelet 1",
                    "color": "Purle",
                    "size": "Small",
                    "unit_price": 5.19,
                    "quantity": -1,
                    "discount": 0.5,
                    "amount": 4.69
                }
            ],
            "sub_total": 86.97,
            "discount": 3,
            "tax": 1.35,
            "total_price": 91.32
        }
    ],

    #4. multiple items receipt. absence of size or color
    {
        "customer_name": "Tom Hanks",
        "auid": 251643191,
        "transaction_id": "autotest004",
        "order_type": "ONLINE",
        "order_timestamp": 1388600500,
        "order_detail": [
            {
                "variation_id": 206609100,
                "description": "MOWGLI SURF The Seventies Mens T-Shirt - White",
                "image": "http://www.tillys.com/tillys/images/catalog/large/206609100.jpg",
                "color": "Black",
                "size": "Large",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            },
            {
                "variation_id": 207527200,
                "description": "IMPERIAL MOTION Flashback Mens Color Changing T-Shirt - Purple",
                "image": "http://www.tillys.com/tillys/images/catalog/thumb/232927750.jpg",
                "color": "Blue",
                "unit_price": 122.99,
                "quantity": 10,
                "amount": 229.9
            }
        ],
        "sub_total": 6386.97,
        "tax": 56.35,
        "total_price": 1561.32,
        "payment": {
            "payment_type": "DEBIT",
            "amount": 300,
            "card_number": "4523321411452025"
        }
    },


    #5. multiple items return receipt.
    [
        {
            "customer_name": "Shanfour Mstrtest",
            "auid": 251643191,
            "transaction_id": "autotest005",
            "order_type": "PHONE",
            "order_timestamp": 1388700600,
            "amount_for_points": 160,
            "order_detail": [
                {
                    "variation_id": 206609100,
                    "description": "LRG Creative Mens Windbreaker - Blue",
                    "image": "http://www.tillys.com/tillys/images/catalog/large/206609100.jpg",
                    "color": "Black",
                    "size": "Large",
                    "unit_price": 23.99,
                    "quantity": 1,
                    "amount": 23.99
                },
                {
                    "variation_id": 207527200,
                    "description": "BROOKLYN CLOTH Mens Varsity Jacket - Charcoal ",
                    "image": "http://www.tillys.com/tillys/images/catalog/thumb/226992110.jpg",
                    "color": "Blue",
                    "unit_price": 22.99,
                    "quantity": 10,
                    "amount": 229.9
                },
                {
                    "variation_id": 204375221,
                    "description": "LEVI'S 511 Mens Skinny Jeans",
                    "image": "http://www.tillys.com/tillys/images/catalog/thumb/228519200.jpg",
                    "size": "28x32",
                    "unit_price": 42.99,
                    "quantity": 4,
                    "discount": 3.00,
                    "amount": 139.99
                },
                {
                    "variation_id": 13110000001,
                    "description": "RVCA Alcatraz Mens Jacket - Black",
                    "unit_price": 5.19,
                    "quantity": 6,
                    "discount": 0.5,
                    "amount": 4.69
                }
            ],
            "sub_total": 1386.97,
            "tax": 56.35,
            "total_price": 401.32,
            "payment": {
                "payment_type": "CREDIT",
                "amount": 300,
                "card_number": "4523321411452025"
            }
        },
        {
            "customer_name": "Shanfour Mstrtest",
            "auid": 251643191,
            "transaction_id": "autotest005",
            "order_type": "PHONE",
            "order_timestamp": 1388800700,
            "order_detail": [
                {
                    "variation_id": 207527200,
                    "description": "RVCA Alcatraz Mens Jacket - Black",
                    "image": "http://www.tillys.com/tillys/images/catalog/thumb/225470131.jpg",
                    "color": "Blue",
                    "unit_price": 22.99,
                    "quantity": -5,
                    "amount": 115.9
                },
                {
                    "variation_id": 204375221,
                    "description": "LEVI'S 511 Mens Skinny Jeans",
                    "image": "http://www.tillys.com/tillys/images/catalog/large/204375221.jpg",
                    "size": "28x32",
                    "unit_price": 42.99,
                    "quantity": -2,
                    "amount": 80.99
                },
                {
                    "variation_id": 13110000001,
                    "description": "VALOR Knoll Mens Vest - Charcoal",
                    "unit_price": 5.19,
                    "quantity": -1,
                    "amount": 5.19
                }
            ],
            "sub_total": 186.97,
            "total_price": 186.32
        },
        {
            "customer_name": "Shanfour Mstrtest",
            "auid": 251643191,
            "transaction_id": "autotest005",
            "order_type": "PHONE",
            "order_timestamp": 1388900700,
            "order_detail": [
                {
                    "variation_id": 207527200,
                    "description": "RETROFIT Kenneth Mens Shirt",
                    "image": "http://microstrat.vo.llnwd.net/o45/alert/uat/50529af13dd9d_5051c24352109_195640100.jpg",
                    "color": "Blue",
                    "unit_price": 22.99,
                    "quantity": -1,
                    "amount": 115.9
                },
                {
                    "variation_id": 204375221,
                    "description": "LEVI'S 511 Mens Skinny Jeans",
                    "image": "http://www.tillys.com/tillys/images/catalog/large/204375221.jpg",
                    "size": "28x32",
                    "unit_price": 42.99,
                    "quantity": -1,
                    "amount": 80.99
                },
                {
                    "variation_id": 13110000001,
                    "description": "Store & single item Bracelet 1",
                    "unit_price": 5.19,
                    "quantity": -1,
                    "amount": 5.19
                }
            ],
            "sub_total": 170,
            "total_price": 170
        }
    ],

    #6. multiple items receipt, no image.
    {
        "customer_name": "Shanfour Mstrtest",
        "auid": 251643191,
        "transaction_id": "autotest006",
        "order_type": "STORE",
        "shop_id": 14,
        "order_timestamp": 1389000800,
        "order_detail": [
            {
                "variation_id": 206609100,
                "description": "RSQ London Mens Destructed Skinny Jeans - Vintage Medium",
                "color": "Black",
                "size": "Large",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            },
            {
                "variation_id": 207527200,
                "description": "RVCA Tribar Mens Thermal - White",
                "color": "Blue",
                "unit_price": 22.99,
                "quantity": 10,
                "amount": 229.9
            },
            {
                "variation_id": 204375221,
                "description": "SHOUTHOUSE Tribal Print Mens Thermal - Oatmeal",
                "size": "28x32",
                "unit_price": 42.99,
                "quantity": 4,
                "discount": 3.00,
                "amount": 139.99
            },
            {
                "variation_id": 13110000001,
                "description": "MICROS Source Mens Hybrid Shorts - Charcoal ",
                "unit_price": 5.19,
                "quantity": 6,
                "discount": 0.5,
                "amount": 4.69
            },
            {
                "variation_id": 206609101,
                "description": "QUIKSILVER Amphibians Scallopuss Mens Hybrid Shorts - Metal ",
                "color": "Black",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            },
            {
                "variation_id": 206609102,
                "description": "VOLCOM Frickin Modern Chino Mens Pants - Khaki ",
                "size": "Large",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            },
            {
                "variation_id": 206609103,
                "description": "ELEMENT Strapped Mens Boardshorts - Blue",
                "color": "Black",
                "size": "Large",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            },
            {
                "variation_id": 206609104,
                "description": "HURLEY One & Only Mens Boardshorts - Hot Pink",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            },
            {
                "variation_id": 206609105,
                "description": "5 YOUNG & RECKLESS Bold Logo Mens T-Shirt",
                "color": "Black",
                "size": "Large",
                "unit_price": 23.99,
                "quantity": 1,
                "amount": 23.99
            }
        ],
        "sub_total": 386.97,
        "tax": 56.35,
        "total_price": 996.2
    }
]