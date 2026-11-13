""" Downloads all relevant data into categorised folders for later selection, inside the i_landing_layer folder"""

# Data has right now been installed by hand. Later additions will include site-specific scraper.
for inst in [
            "https://www.wheeloratings.com/489c43a1-ad8c-456b-b1e6-a755c78e2e95",
            
            ]:

    print("Downloading from", inst, "to i_landing_layer")
    