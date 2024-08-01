document.addEventListener("DOMContentLoaded", function () {
  const addIngredientButton = document.getElementById("add-ingredient");
  const ingredientInputs = document.getElementById("ingredient-inputs");
  let ingredientCounter = 3;

  addIngredientButton.addEventListener("click", function () {
    ingredientCounter++;
    const newIngredientInput = document.createElement("div");
    newIngredientInput.classList.add("ingredient");
    newIngredientInput.innerHTML = `
      <input type="text" name="ingredients[]" placeholder="Ingredient ${ingredientCounter}">
    `;
    ingredientInputs.appendChild(newIngredientInput);
  });

  document.querySelectorAll(".add-to-menu-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const button = form.querySelector("button");
      button.disabled = true;

      const formData = new FormData(form);

      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const isAdded = button.textContent.trim() === "Add to Menu";
        button.textContent = isAdded ? "Remove from Menu" : "Add to Menu";
        button.classList.toggle("remove-from-menu-btn");
        button.classList.toggle("add-to-menu-btn");
      } else {
        alert("Failed to add/remove recipe from menu. Please try again later.");
      }
      button.disabled = false;
    });
  });
});
