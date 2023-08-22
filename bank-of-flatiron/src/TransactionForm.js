// TransactionForm.js
import React, { useState } from 'react';

function TransactionForm({ onAddTransaction }) {
  const [date, setDate] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const newTransaction = {
      date,
      description,
      category,
      amount: parseFloat(amount),
    };

    onAddTransaction(newTransaction);

    // Clear form fields
    setDate('');
    setDescription('');
    setAmount('');
  };

  return (
    <div className="transaction-form">
      <h2>New Transaction</h2>
      <table>
        <tbody>
          <tr>
            <td><label>Date:</label></td>
            <td>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </td>
          </tr>
          <tr>
            <td><label>Description:</label></td>
            <td>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </td>
          </tr>
          <tr>
          <td><label>Category:</label></td>
            <td>
              <input
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                required
              />
            </td>
          </tr>
          <tr>
            <td><label>Amount:</label></td>
            <td>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </td>
          </tr>
          <tr>
            <td colSpan="2">
              <button type="submit" onClick={handleSubmit}>Add Transaction</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default TransactionForm;
