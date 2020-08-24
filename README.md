# FileDrop

## Description

This is a simple Flask application that allows you to host a Dropzone for files.

Basically you can specify a bucket name and upload files to that bucket.

Downloading the files from a bucket can only be done when the bucket name is known.

This is not for using in a high security setting, but for a quick solution that allows you to drop files from anywhere and have them available afterwards.

Uploads will be deleted after 30 days.

## Usage
`docker run -p 5000:5000 -v /path/to/drop/on/host:/uploads muyajil/filedrop:latest`

```
filedrop:
    image: muyajil/filedrop:latest
    ports:
      - 5000:5000
    volumes:
      - "path/to/drop/on/host:/uploads"
```