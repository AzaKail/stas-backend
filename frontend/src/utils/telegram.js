export function telegramBuyLink({ managerUsername, productUrl, productTitle, variantText, price }) { //Нормальная ссылка в диалог к менеджеру по продажам.
    const parts = [
    "Здравствуйте! Меня заинтересовал товар:",
    productTitle,
  ];

  if (variantText) parts.push(`Вариант: ${variantText}`);
  if (price !== undefined && price !== null) parts.push(`Цена: ${price} ₽`);

  parts.push(`Ссылка: ${productUrl}`);

  if (managerUsername) {
    const username = managerUsername.replace(/^@/, "");
    parts.push(`Менеджер: https://t.me/${username}`);
  }

  const text = parts.filter(Boolean).join("\n");

  return `https://t.me/share/url?url=${encodeURIComponent(productUrl)}&text=${encodeURIComponent(text)}`;
}
