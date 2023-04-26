// SPDX-License-Identifier: MIT
// Import the SafeMath library for secure integer arithmetic
// This contract defines an ERC721 token interface for non-fungible tokens
pragma solidity ^0.8.0;

// Define the ERC721 contract as an abstract contract, since it is intended to be inherited by other contracts
abstract contract ERC721 {
  // Define two events for transfer and approval of tokens
  event Transfer(address indexed _from, address indexed _to, address _deviceAddress);
  event Approval(address indexed _owner, address indexed _approved, address _deviceAddress);

  // Define four functions that must be implemented by contracts that inherit from this interface
  function balanceOf(address _owner) public view virtual returns (uint256 _balance);
  function ownerOf(address _deviceAddress) public view virtual returns (address _owner);
  function transfer(address _to, address _deviceAddress) public virtual ;
  function approve(address _to, address _deviceAddress) public virtual ;
  function takeOwnership(address _deviceAddress) public virtual ;
}