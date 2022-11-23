function checkout() {
  fetch("/config/")
    .then((result) => {
      return result.json();
    })
    .then((data) => {
      const stripe = Stripe(data.publicKey);
      fetch(`/checkout/`)
        .then((result) => {
          return result.json();
        })
        .then((data) => {
          return stripe.redirectToCheckout({ sessionId: data.sessionId });
        })
        .then((res) => console.log(res))
        .catch((error) => console.log(error));
    });
}
