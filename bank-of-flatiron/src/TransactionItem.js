import React from 'react';

function TransactionItem({ transaction, onDeleteTransaction }) {
  const handleDelete = () => {
    onDeleteTransaction(transaction.id);
  };

  return (
    <tr>
      <td>{transaction.date}</td>
      <td>{transaction.description}</td>
      <td>{transaction.category}</td>
      <td>${transaction.amount.toFixed(2)}</td>
      <td>
        <button onClick={handleDelete}>Delete</button>
      </td>
    </tr>
  );
};

export default TransactionItem;
