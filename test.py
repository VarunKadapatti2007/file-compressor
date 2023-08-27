from flask import Flask, render_template, request, send_file
import cloudconvert

app = Flask(__name__)

cloudconvert.configure(api_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMWZiNmQ2YWYwNmM4MDJlNjM5YjgzNGYzZjFkNzQyM2M4Mzg2NzBjNGUxNjgxNDZkODYwYjcwZWMxMTAxYzYzN2M3MmY1ZDk2Mzg0Y2EwN2QiLCJpYXQiOjE2OTMxMzM5MTUuODA2MTYxLCJuYmYiOjE2OTMxMzM5MTUuODA2MTYyLCJleHAiOjQ4NDg4MDc1MTUuODAyMDYxLCJzdWIiOiI2MzU4MDUzNSIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwid2ViaG9vay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.VaaWPQX2no8uKjrKJLDFh5btiooTtcj4w2QfsFG-luQGQljfZvl4O5N2ZE7wa6uA83iWrfSOXR5BzkZUSaCAIfp_222IwCgp3hJ2Uo-i55RyVdXjDNVqz5Yhm81k-k6kVouNZnQiNdURw15VHsACjRQVnhvwhbbGBgMDejX7b00Rf_vR0Q8Xte5VXQroFe_fnVk5fiKQjZ0Z3IwGb1ckaVoDyksjkIgs0cqHG-7QS4p1Hv2DZoqI6nX-AWruMUqZQ9jYGjuguNDVla9X9WHOcqu-7qu7lCv0mG43Hll9G0C9UvfCQg-_8dYJasg-EgoBPaq6Qcci9WVcSIV8ANd7A2pZkq9kFhfORpjbx415fxtiYeIE8Qq-Oa9ed2ZpwPtGFSMHy9SNFS2WwNf2GW-n0Vo_HysfSzKvjkRaplkvBuS9me3zy8x-nqulyfnyhKxar6jMet96yzjJngGRIbrQO_g762NI5xCyrLfMgJVKVEuvXpQHECNBX2BBpJTzEoz4tGfvouQysbHlWSx6iPqOSIZ6_g-7KUBe3ojDjmdGqqLa6v96-5mp4slzdYePv18P5GJaFhikWTUAvUyuAoMLRIpoBnYLQoKQc6jFFOgaXY8oiJl4uGhcfzXqzRcO7SPiRg2Vco376QFNYTjqhWfHMU8kgtaLuC0nJ6bGA-O9INI', sandbox=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    job = cloudconvert.Job.create(payload={
        "tasks": {
            'upload-my-file': {
                'operation': 'import/upload'
            }
        }
    })

    if 'tasks' in job and isinstance(job['tasks'], dict):
        upload_task_id = list(job['tasks'].keys())[0]
        upload_task = cloudconvert.Task.find(id=upload_task_id)
        uploaded_file = request.files['file']

        temp_file_path = 'E:\\file_convert\\uploads\\' + uploaded_file.filename
        uploaded_file.save(temp_file_path)

        res = cloudconvert.Task.upload(file=temp_file_path, task=upload_task)

        exported_url_task_id = job['tasks'][upload_task_id]['output']['tasks'][0]['id']
        res = cloudconvert.Task.wait(id=exported_url_task_id)
        file = res.get("result").get("files")[0]
        res = cloudconvert.download(filename=file['filename'], url=file['url'])

        return send_file(
            res,
            as_attachment=True,
            download_name='compressed.pdf'
        )
    else:
        return "Error: Unable to retrieve task information from the CloudConvert API"

if __name__ == '__main__':
    app.run(debug=True)
