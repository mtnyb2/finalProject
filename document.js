document.addEventListener('DOMContentLoaded', function () {
    // Example: Fetch the items from your Flask backend
    fetch('/path-to-your-endpoint')
        .then(response => response.json())
        .then(data => {
            const selectElement = document.getElementById('purchaseItemSelect');
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id; // Assuming each item has an ID
                option.textContent = item.name; // Assuming each item has a name
                selectElement.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading items:', error));
});

document.getElementById('addTicketForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent default form submission

    const selectedItemId = document.getElementById('purchaseItemSelect').value;
    const comment = document.getElementById('ticketComment').value;

    // Construct the form data to send
    const formData = {
        itemId: selectedItemId,
        comment: comment
    };

    // Send the data to your Flask backend
    fetch('/path-to-your-ticket-submission-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
        .then(response => response.json())
        .then(data => console.log('Ticket submitted successfully:', data))
        .catch(error => console.error('Error submitting ticket:', error));
});


// For fetching items
fetch('/api/items')
    .then(/* existing code */)

// For submitting the form
fetch('/api/submit-ticket', {
    method: 'POST',
    /* existing code */
})

fetch('/api/users/<user_id>')
    .then(response => response.json())
    .then(data => {
        document.getElementById('firstName').value = data.first_name;
        document.getElementById('lastName').value = data.last_name;
        document.getElementById('address').value = data.address;
    });


fetch('/api/orders/<order_id>')
    .then(response => response.json())
    .then(data => {
        // Populate fields or lists with order data
        document.getElementById('orderNumber').value = data.order_number;
        const itemsList = document.getElementById('itemsList');
        data.items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = item;
            itemsList.appendChild(listItem);
        });
    });

fetch('/api/problem-types')
    .then(response => response.json())
    .then(data => {
        const selectElement = document.getElementById('problemType');
        data.forEach(problemType => {
            const option = document.createElement('option');
            option.value = problemType;
            option.textContent = problemType;
            selectElement.appendChild(option);
        });
    });


//new customer
document.getElementById('newCustomerForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Collecting form data
    const formData = {
        id: document.getElementById('customerId').value,
        name: document.getElementById('customerName').value,
        phone_number: document.getElementById('customerPhoneNumber').value,
        email: document.getElementById('customerEmail').value,
        address: document.getElementById('customerAddress').value,
        age: document.getElementById('customerAge').value,
    };

    // Sending the form data to the Flask backend
    fetch('/customers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Customer added successfully');
            // Optionally reset the form or redirect the user
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error adding customer');
        });
});


