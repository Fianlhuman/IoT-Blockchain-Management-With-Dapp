// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "Ownable.sol";
import "SafeMath.sol";

// Define the DeviceFactory contract, which creates and manages devices
contract DeviceFactory is Ownable {
  // Import the SafeMath library for secure integer arithmetic
  using SafeMath for uint256;

  // Define an event that is emitted when a new device is created
  event NewDevice(address deviceAddress);

  // Define a struct to represent a device, which stores its Ethereum address
  struct Device {
    address deviceAddress;
    //string name;  // Not used in this version of the contract
  }

  // Store all devices that have been created in an array
  Device[] public devices;

  // Define two mappings to keep track of the owner of each device
  // deviceToOwner maps a device's Ethereum address to its owner's Ethereum address
  // ownerToDevices maps an owner's Ethereum address to an array of their device's Ethereum addresses
  mapping (address => address) public deviceToOwner;
  mapping (address => address[]) public ownerToDevices;

  // Define a modifier that restricts access to a function to the owner of a specified device
  modifier onlyOwnerOf(address _deviceAddress) {
    require(msg.sender == deviceToOwner[_deviceAddress], "Only device owner can perform this action.");
    _;
  }

  // Define a function to create a new device with a given Ethereum address
  function createDevice(address _deviceAddress) public {
    // Require that the specified device does not already exist
    require(deviceToOwner[_deviceAddress] == address(0), "Device already exists.");
    
    // Add the new device to the devices array
    devices.push(Device(_deviceAddress));
    
    // Set the device's owner to the address of the caller of the function
    deviceToOwner[_deviceAddress] = msg.sender;
    
    // Add the device's Ethereum address to the array of devices owned by its owner
    ownerToDevices[msg.sender].push(_deviceAddress);
    
    // Emit an event to indicate that a new device has been created
    emit NewDevice(_deviceAddress);
  }
}
