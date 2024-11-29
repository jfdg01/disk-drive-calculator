/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1045062673")

  // update field
  collection.fields.addAt(3, new Field({
    "hidden": false,
    "id": "number3459605862",
    "max": null,
    "min": null,
    "name": "main_stat_level",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1045062673")

  // update field
  collection.fields.addAt(3, new Field({
    "hidden": false,
    "id": "number3459605862",
    "max": 15,
    "min": 0,
    "name": "main_stat_level",
    "onlyInt": true,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
})
