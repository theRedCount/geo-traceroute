import subprocess
import re
import requests
import folium
from collections import defaultdict

# Function to execute traceroute and capture output
def run_traceroute(destination_ip):
    try:
        result = subprocess.run(
            ["traceroute", destination_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(f"Traceroute error: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Error running traceroute: {e}")
        return None

# Function to extract IP addresses from traceroute output (excluding first two lines)
def extract_ips(traceroute_output):
    lines = traceroute_output.strip().split("\n")
    # Skip the first line (traceroute summary) and the first hop
    if len(lines) > 2:
        lines = lines[2:]
    else:
        print("Not enough data in traceroute output.")
        return []
    # Extract IPs from the remaining lines
    ips = []
    for line in lines:
        match = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
        if match:
            ips.append(match[0])
    return ips

# Function to get geographic data for an IP
def get_geo_data(ip):
    url = f"https://ipinfo.io/{ip}/geo"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "loc" in data:
                lat, lon = map(float, data["loc"].split(","))
                city = data.get("city", "Unknown City")
                country = data.get("country", "Unknown Country")
                return {"ip": ip, "lat": lat, "lon": lon, "city": city, "country": country}
    except Exception as e:
        print(f"Error geolocating IP {ip}: {e}")
    return None

# Function to group data by location
def group_by_location(geo_data_list):
    location_map = defaultdict(list)
    for step, geo_data in enumerate(geo_data_list, start=1):
        key = (geo_data["lat"], geo_data["lon"])
        location_map[key].append({"step": step, "ip": geo_data["ip"], "city": geo_data["city"], "country": geo_data["country"]})
    return location_map

# Function to generate map with lines and grouped markers
def generate_map_with_lines_and_legend(geo_data_list, output_map="traceroute_map.html"):
    if not geo_data_list:
        print("No valid geographic data to plot.")
        return None

    # Group data by location
    grouped_locations = group_by_location(geo_data_list)

    # Create a map centered on the first IP location
    first_location = geo_data_list[0]
    m = folium.Map(location=[first_location["lat"], first_location["lon"]], zoom_start=4)
    
    # Add grouped markers
    coordinates = []
    for (lat, lon), entries in grouped_locations.items():
        coordinates.append((lat, lon))
        popup_content = "<b>Location:</b> {}<br><b>IPs:</b><ul>".format(entries[0]["city"])
        for entry in entries:
            popup_content += f"<li>Step {entry['step']}: {entry['ip']}</li>"
        popup_content += "</ul>"
        folium.Marker(
            [lat, lon],
            popup=popup_content
        ).add_to(m)
    
    # Add a line connecting all the markers
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)
    
    # Add a legend with all IPs and steps
    legend_html = '<div style="position: fixed; bottom: 50px; left: 50px; width: 300px; height: auto; \
                    background-color: white; border:2px solid grey; z-index:9999; font-size:14px;"> \
                    <b>Traceroute Steps:</b><br><ul>'
    for step, geo_data in enumerate(geo_data_list, start=1):
        legend_html += f"<li>Step {step}: {geo_data['ip']} ({geo_data['city']}, {geo_data['country']})</li>"
    legend_html += "</ul></div>"
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save the map to an HTML file
    m.save(output_map)
    print(f"Map saved as {output_map}")

# Main function
def main():
    destination_ip = input("Enter the destination IP address: ")

    # Run traceroute
    print(f"Running traceroute to {destination_ip}...")
    traceroute_output = run_traceroute(destination_ip)
    if not traceroute_output:
        print("Failed to perform traceroute.")
        return

    # Extract IPs from traceroute output
    ips = extract_ips(traceroute_output)
    print(f"Extracted IPs: {ips}")

    # Get geographic data for each IP
    geo_data_list = []
    for ip in ips:
        geo_data = get_geo_data(ip)
        if geo_data:
            geo_data_list.append(geo_data)
    print(f"Geographic Data: {geo_data_list}")

    # Generate map with lines connecting markers and a legend
    generate_map_with_lines_and_legend(geo_data_list)

if __name__ == "__main__":
    main()
