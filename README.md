# Geo-Traceroute

**Geo-Traceroute** is a tool that combines the `traceroute` command with an interactive geographic visualization. Using geolocation data for IP addresses, it generates an HTML map that displays the network path to a specific destination, with markers and lines to represent each hop.

## Features
- Executes the `traceroute` command to obtain intermediate nodes to a destination IP.
- Excludes the first two IPs (the first hop and the summary).
- Geolocates IPs using the [ipinfo.io](https://ipinfo.io/) API.
- Generates an HTML map with:
  - **Unique markers** for each city.
  - **Popups** with information about IPs and their associated steps.
  - **Lines** connecting the markers in sequential order.
  - **Legend** listing all IP addresses and their steps in order.

## Requirements
- Python 3.7 or higher.
- Required Python modules:
  - `requests`
  - `folium`
- The `traceroute` command must be installed and configured on your operating system.

### Installing Modules
You can install the required modules by running:
```bash
pip install requests folium
```

### Installing Traceroute
#### Linux (Debian/Ubuntu)
```bash
sudo apt install traceroute
```

#### macOS (via Homebrew)
```bash
brew install traceroute
```

#### Windows
Install `tracert`, which is already included in Windows.

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/theRedCount/geo-traceroute.git
   cd geo-traceroute
   ```
2. Run the script:
   ```bash
   python geo_traceroute.py
   ```
3. Enter the destination IP address or hostname when prompted.

### Example Execution
If you enter the IP address `8.8.8.8`:
- The script will run `traceroute` to `8.8.8.8`.
- Geolocate the intermediate IPs.
- Generate an HTML map (`traceroute_map.html`) in the current directory.

Open the HTML file in a browser to view the interactive map.

## Output
The map includes:
- Markers representing the cities traversed during the traceroute.
- Popups displaying the IPs and their associated steps.
- A blue line connecting the markers to represent the path.
- A legend listing all IPs and steps in order.

## Screenshot
![Example Map](screenshot.png)

## Notes
- To get accurate data, the script uses the free API from [ipinfo.io](https://ipinfo.io/). If you exceed the free version limits, you can register for an API key.
- Ensure the `traceroute` command is properly configured on your system.

## License
This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions
Contributions are welcome! Please:
1. Fork the project.
2. Create a branch for your changes: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

## Author
Created by **theRedCount** with love. For questions or suggestions, feel free to contact me via GitHub.

