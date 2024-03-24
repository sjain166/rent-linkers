import React, { useState } from "react";
import "./customerForm.css";
import { sendInput } from "./util";
import { useToast } from "@chakra-ui/react";

const ProductForm = ({ wallet }) => {
  const [price, setPrice] = useState(0);
  const [duration, setDuration] = useState(0);
  const [rating, setRating] = useState(0);
//   const [productName, setProductName] = useState("");
  const toast = useToast();

  async function createItem() {
    await sendInput(
      JSON.stringify({
        "method": "addItem",
        "item": {
          "duration": duration.toString(),
          "rating": rating.toString(),
          "price": price.toString(),
        },
      }),
      wallet,
      toast
    );
  }

  async function handleSubmit(e) {
    e.preventDefault();
    await createItem();
    // Handle form submission here, for example, you can send the formData to an API
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        {/* <label htmlFor="productName">Product Name:</label>
        <input
          type="text"
          id="productName"
          name="productName"
          value={productName}
          onChange={(e) => setProductName(productName)}
          required
        /> */}
      </div>
      <div>
        <label htmlFor="productDescription">Price:</label>
        <input
          id="price"
          name="price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="priceRange">Duration (In Months):</label>
        <input
          id="duration"
          name="duration"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="condition">Rating (out of 10):</label>
        <input
          id="rating"
          name="rating"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
          required
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default ProductForm;
