document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("product-form");
  const tableBody = document.querySelector("#product-table tbody");
  const errorMessageDiv = document.getElementById("error-message");
  const successMessageDiv = document.getElementById("success-message");

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);
    const data = {
      name: formData.get("name"),
      description: formData.get("description"),
      price: parseFloat(formData.get("price")),
    };

    errorMessageDiv.textContent = "";
    successMessageDiv.textContent = "";

    fetch("/products/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((errorData) => {
            throw new Error(JSON.stringify(errorData));
          });
        }
        return response.json();
      })
      .then((data) => {
        if (data["success-message"]) {
          successMessageDiv.textContent = data["success-message"];
          form.reset();
          loadProducts();
        }
      })
      .catch((error) => {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData["error-message"]) {
            let errorMessages = "";
            for (const field in errorData["error-message"]) {
              if (errorData["error-message"].hasOwnProperty(field)) {
                errorData["error-message"][field].forEach((errObj) => {
                  errorMessages += `${errObj.message}<br>`;
                });
              }
            }
            errorMessageDiv.innerHTML = errorMessages.trim();
          }
        } catch (e) {
          console.error("Ошибка при обработке ошибок:", e);
          errorMessageDiv.textContent = "Произошла ошибка. Попробуйте еще раз.";
        }
      });
  });

  function loadProducts() {
    fetch("/products/")
      .then((response) => response.json())
      .then((products) => {
        tableBody.innerHTML = "";
        products.forEach((product) => {
          const row = document.createElement("tr");
          row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                `;
          tableBody.appendChild(row);
        });
      })
      .catch((error) => {
        console.error("Ошибка:", error);
      });
  }

  loadProducts();
});
