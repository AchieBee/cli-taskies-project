import React, { useState, useEffect } from 'react';
import './App.css'; // You can create your own CSS file for styling

import TransactionList from './TransactionList';
import TransactionForm from './TransactionForm';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Fetch data from the local server (replace with your API call)
    fetch('http://localhost:8001/transactions')
      .then(response => response.json())
      .then(data => setTransactions(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const handleAddTransaction = (newTransaction) => {
    setTransactions([...transactions, newTransaction]);
  };

  const filteredTransactions = transactions.filter(transaction =>
    transaction.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeleteTransaction = (transactionId) => {
    const updatedTransactions = transactions.filter(transaction => transaction.id !== transactionId);
    setTransactions(updatedTransactions);
  }

  return (
    <div className="App">
    <h1 className='Header'>Flatiron Bank</h1>
    <TransactionForm onAddTransaction={handleAddTransaction} />
    <input
      type="text"
      placeholder="Search transactions by description..."
      value={searchTerm}
      onChange={e => setSearchTerm(e.target.value)}
    />
    <TransactionList transactions={filteredTransactions}  onDeleteTransaction={handleDeleteTransaction}/>
    </div>
  )
};
export default App;