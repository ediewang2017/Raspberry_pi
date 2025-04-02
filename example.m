% Define a 16-bit value (e.g., all bits set)
value = hex2dec('FFFF');  % You can also use any integer between 0 and 65535
hexStr = upper(dec2hex(value, 4));  % Convert to 4-digit uppercase hex string (e.g., 'FFFF')

% Define the hostname or IP address of the Raspberry Pi
host = 'http://127.0.0.1:5000';  % Use your Pi's hostname or IP address

% Construct the full URL for the request
url = sprintf('%s/%s', host, hexStr);

% Send the GET request to the Flask server
try
    response = webread(url);  % Read the JSON response

    % Display the result
    fprintf("✅ Server response:\n");
    fprintf("Binary:   %s\n", response.message);
    fprintf("Hex:      %s\n", response.hex);
    fprintf("Decimal:  %d\n", response.dec);
catch ME
    % Handle any errors (e.g., server not reachable)
    fprintf("❌ Failed to reach server at %s\n", url);
    fprintf("%s\n", ME.message);
end