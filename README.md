Notes on the proxy:

-The state variables cannot be removed or have their order changed. This is due to Storage Clashes.

This specific proxy pattern combats the issue of Function Selector Clashes by only allowing admin to call admin functions and other users to only call non-admin (non-proxy) functions.

"
If the caller is the admin of the proxy, the proxy will not delegate any calls, and will only answer management messages it understands.
If the caller is any other address, the proxy will always delegate the call, no matter if it matches one of the proxy’s own functions.
"

- Cannot use constructors when using this pattern, need to have an "initialize" method which is passed to the proxy when deploying/upgrading.
    Take care with initializer methods, they should only be called once and will need a require to stop it being called > 1 times. (See Initializable OpenZeppelin contract)

OpenZeppelin: https://blog.openzeppelin.com/the-transparent-proxy-pattern/