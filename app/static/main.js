const savedListDiv = document.querySelector("#savedlist");
const bottomAlert = document.querySelector("#alertText");
const bottomAlertDiv = document.querySelector(".myAlert-bottom");

const displayAlert = (text) => {
  bottomAlert.textContent = text;
  bottomAlertDiv.style.display = "block";
  setTimeout(function () {
    bottomAlert.textContent = "";
    bottomAlertDiv.style.display = "none";
  }, 2000);
};

const addToCompare = (elem, item_id) => {
    const data = { item_id: item_id }
    fetch('/compare_cart',{
      method:'POST',
      headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
      if(data.message){
        displayAlert(`Saved to session`);
        elem.style.display = "none";
      }else{
        displayAlert(`Could not be saved. Please try again.`);
      }
    })
    .catch(data => console.log("error"))
}

const clearProduct = (elem, item_id) => {
  const data = { item_id: item_id }
  fetch('/compare_cart',{
    method:'DELETE',
    headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(data => {
    if(data.message){
      productContainer = elem.parentNode.parentNode.parentNode;
      productContainer.style.opacity = '0';
      setTimeout(function()
        {
            productContainer.parentNode.removeChild(productContainer);
            displayAlert(`Deleted`);
      }, 1000);
    }else{
      displayAlert(`Could not delete. Please try again.`);
    }
  })
  .catch(data => console.log("error"))

};

const clearCompare = () => {
  fetch('/compare_cart',{
    method:'DELETE'
  })
  .then(res => res.json())
  .then(data => {
    if(data.message){
      displayAlert(`Cleared saved items`);
    }else{
      displayAlert(`Could not delete. Please try again.`);
    }
  })
  .catch(data => console.log("error"))

  savedListDiv.parentNode.removeChild(savedListDiv);
}

const addToWatchlist = (elem, item_id, user_id, current_price) => {
  watchlistDiv = elem.parentNode;
  inputElem = watchlistDiv.querySelector('input')
  desiredPrice = Number(inputElem.value);
  if (!desiredPrice){
    displayAlert(`Input the desired amount`);
    return;
  }else if (current_price <= desiredPrice){
    displayAlert(`Desired amount must be lower than current price`);
    return;
  }
  else{
    data = {
      item_id : item_id,
      user_id : user_id,
      desired_price: desiredPrice
    }
    fetch('/watchlist',{
      method:'POST',
      headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
      if(data.message){
        displayAlert(`Added to watchlist`);
        elem.style.display = "none";
        inputElem.style.display = "none";
      }else{
        console.log(data)
        displayAlert(`Could not add. Please try again.`);
      }
    })
    .catch(data => console.log("error"+data))
  }
}

const removeFromWatchlist = (elem, item_id, user_id) =>{
  data = {
    item_id : item_id,
    user_id : user_id
  }
  fetch('/watchlist',{
    method:'DELETE',
    headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(data => {
    if(data.message){
      productContainer = elem.parentNode.parentNode.parentNode;
      productContainer.style.opacity = '0';
      setTimeout(function()
        {
            productContainer.parentNode.removeChild(productContainer);
            displayAlert(`Deleted`);
      }, 1000);
    }else{
      console.log(data)
      displayAlert(`Could not add. Please try again.`);
    }
  })
  .catch(data => console.log("error"+data))
}

const updateWatchlist = (elem, item_id, user_id) =>{
  watchlistDiv = elem.parentNode;
  prodDescription = watchlistDiv.parentNode;

  currentPriceElem = prodDescription.querySelector('.currentPrice')
  currentPrice = Number(currentPriceElem.value)
  currentDesiredElem = prodDescription.querySelector('.desiredPrice')
  inputElem = watchlistDiv.querySelector('input')
  updatedPrice = Number(inputElem.value)
  if (!updatedPrice){
    displayAlert(`Input the desired amount`);
    return;
  }else if(updatedPrice>=currentPrice){
    displayAlert(`Desired amount must be lower than current price`);
    return;
  }
  else{
    data = {
      item_id : item_id,
      user_id : user_id,
      updated_price: updatedPrice
    }
    fetch('/watchlist',{
      method:'PUT',
      headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
      if(data.message){
        displayAlert(`Added to watchlist`);
        inputElem.value = ''
        currentDesiredElem.textContent = updatedPrice
      }else{
        console.log(data)
        displayAlert(`Could not add. Please try again.`);
      }
    })
    .catch(data => console.log("error"+data))
  }
}