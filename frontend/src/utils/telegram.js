export function telegramBuyLink({ managerUsername, productUrl, productTitle, variantText, price }) {
  const text =
    `Здравствуйте! Меня заинтересовал товар:\n` +
    `${productTitle}\n` +
    (variantText ? `Вариант: ${variantText}\n` : "") +
    (price ? `Цена: ${price} ₽\n` : "") +
    `Ссылка: ${productUrl}`;

  // Надёжно открывается почти везде
  return `https://t.me/share/url?url=${encodeURIComponent(productUrl)}&text=${encodeURIComponent(text)}`;
}
