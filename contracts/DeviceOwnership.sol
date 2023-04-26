// SPDX-License-Identifier: MIT
// Import the SafeMath library and DeviceFactory contract
// This contract defines a contract for ownership of non-fungible devices based on the ERC721 token standard
pragma solidity ^0.8.0;

import "./SafeMath.sol";
import "./DeviceFactory.sol";
import "./erc721.sol";

// Define the DeviceOwnership contract, which inherits from both DeviceFactory and ERC721
contract DeviceOwnership is DeviceFactory, ERC721 {

  using SafeMath for uint256;

  // Define two mappings to store device approvals and owner public keys
  mapping (address => address) private deviceApprovals;
  mapping (address => string)  private ownerToPublicKey;

  // Define a function to set the public key of the calling owner
  function setPublicKey(string memory _publicKey) public{
      ownerToPublicKey[msg.sender]= _publicKey;
  }

  // Define a function to retrieve the public key of an owner
  function getPublicKey(address _owner) public view returns (string memory) {
      return ownerToPublicKey[_owner];
  }

  // Implement the balanceOf function from the ERC721 interface, which returns the number of devices owned by an address
  function balanceOf(address _owner) public view override returns (uint256 _balance) {
    return ownerToDevices[_owner].length;
  }

  // Implement the ownerOf function from the ERC721 interface, which returns the owner of a device address
  function ownerOf(address _deviceAddress) public view override returns (address _owner) {
    return deviceToOwner[_deviceAddress];
  }

  // Define a private function to transfer ownership of a device
  function _transfer(address _from, address _to, address _deviceAddress) private {
    // Update the device owner mapping
    deviceToOwner[_deviceAddress] = _to;

    // Find and remove the device from the sender's device list
    uint numOfDevices = ownerToDevices[_from].length;
    for (uint i = 0; i < numOfDevices; i++) {
        if (ownerToDevices[_from][i] == _deviceAddress) {
            // Replace the device to remove with the last device in the array
            ownerToDevices[_from][i] = ownerToDevices[_from][numOfDevices - 1];
            
            // Decrease the array length by 1
            ownerToDevices[_from].pop();
            
            break;
        }
    }

    // Add the device to the recipient's device list
    ownerToDevices[_to].push(_deviceAddress);
    
    // Emit a Transfer event to signify the device ownership transfer
    emit Transfer(_from, _to, _deviceAddress);
  }

  // Implement the transfer function from the ERC721 interface, which allows the owner to transfer ownership of a device
  function transfer(address _to, address _deviceAddress) public override onlyOwnerOf(_deviceAddress) {
    _transfer(msg.sender, _to, _deviceAddress);
  }

  // Implement the approve function from the ERC721 interface, which allows the owner to approve a third party to take ownership of a device
  function approve(address _to, address _deviceAddress) public override onlyOwnerOf(_deviceAddress) {
    deviceApprovals[_deviceAddress] = _to;
    emit Approval(msg.sender, _to, _deviceAddress);
  }

  // Implement the takeOwnership function from the ERC721 interface, which allows a third party to take ownership of a device if approved
  function takeOwnership(address _deviceAddress) public override {
    require(deviceApprovals[_deviceAddress] == msg.sender);
    address owner = ownerOf(_deviceAddress);
    _transfer(owner, msg.sender, _deviceAddress);
  }
}