PROJECT=Triangulator
BUCKET=none



project: setup.env data.download
backup: setup.save data.upload
clean: data.clean setup.clean



setup.save:
	 conda env export -n $(PROJECT) --from-history > $(PROJECT).yml
	 git add $(PROJECT).yml
	 git commit -m "backup project conda env .yml"
	 git push

setup.env:
	 conda env create --name $(PROJECT) --file $(PROJECT).yml


data.download:
	 mkdir -p data
	 gsutil rsync -r gs://$(BUCKET) data

data.upload:
	 gsutil rsync -r data gs://$(BUCKET)



setup.clean:
	 conda env remove -n $(PROJECT)

data.clean:
	 mkdir -p data
	 rm -r data
