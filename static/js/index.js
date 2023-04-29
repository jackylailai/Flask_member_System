const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const name = form.elements.name.value.trim();
  const email = form.elements.email.value.trim();
  const password = form.elements.password.value.trim();

  if (!name || !email || !password) {
    alert('請填寫所有欄位');
    return;
  }

  // 將表單數據交給伺服器
  // ...
});
