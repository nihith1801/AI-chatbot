import pyvts
import asyncio

plugin_info = {
    "plugin_name": "start pyvts",
    "developer": "Genteki",
    "authentication_token_path": "./token.txt"
}

async def main():
    vts = pyvts.vts(plugin_info=plugin_info)
    await vts.connect()
    
    print("Connected to VTube Studio")
    
    await vts.request_authenticate_token()  # get token
    await vts.request_authenticate()  # use token
    
    new_parameter_name = "start_parameter"
    await vts.request(
        vts.vts_request.requestCustomParameter(new_parameter_name)
    )  # add new parameter
    
    await vts.close()

if __name__ == "__main__":
    asyncio.run(main())
