all_files = []
    for child in listdir(app.config["UPLOADED_IMAGES_DEST"]):
        if isfile(child):
            all_files.append(child)