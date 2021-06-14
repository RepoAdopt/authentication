from time import sleep
from requests import post, get, patch
from os import getenv

MAX_RETRIES = int(getenv("GATEWAY_RETRIES"))


def establish_gateway_connection(attempts=0):
    if attempts >= MAX_RETRIES:
        return

    name = "authentication"
    upstream_name = f"{name}_upstream"
    base_url = f'http://{getenv("GATEWAY")}'
    service_url = f"{base_url}/services/{name}"
    upstream_url = f"{base_url}/upstreams/{upstream_name}"

    try:
        service_res = get(url=service_url)

        if service_res.status_code == 404:
            # Create the Kong service
            create_service_res = post(
                url=f"{base_url}/services",
                data={"name": name, "url": base_url},
            )

            if create_service_res.status_code == 201:
                print("Kong: Service created")
            else:
                raise Exception("Kong: Failed to create service")

            # Create the upstream
            create_upstream_res = post(
                url=f"{base_url}/upstreams", data={"name": upstream_name}
            )
            if create_upstream_res.status_code == 201:
                print("Kong: Upstream created")
            else:
                raise Exception("Kong: Failed to create upstream")

            # Link upstream
            link_upstream_res = patch(url=service_url, data={"host": upstream_name})
            if link_upstream_res.status_code == 200:
                print("Kong: Upstream linked")
            else:
                raise Exception("Kong: Failed to link upstream to service")

            # Create the route
            create_route_res = post(
                url=f"{service_url}/routes",
                data={"name": "signin", "paths[]": "/signin", "strip_path": "false"},
            )
            if create_route_res.status_code == 201:
                print("Kong: Route added")
            else:
                raise Exception("Kong: Failed to create route")

        # Add target
        res = post(
            url=f"{upstream_url}/targets", data={"target": getenv("AUTHENTICATION_URL")}
        )

        if res.status_code == 200 or res.status_code == 409:
            print("Kong: Created target. Connection established")
            return
        else:
            print("Kong: Failed to create target")

    except Exception as error:
        print(error)

    sleep(0.2)
    establish_gateway_connection(attempts=attempts + 1)
