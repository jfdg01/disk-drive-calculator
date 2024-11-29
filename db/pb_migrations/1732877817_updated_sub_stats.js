/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3743999371")

  // update field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "number2599078931",
    "max": null,
    "min": null,
    "name": "level",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3743999371")

  // update field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "number2599078931",
    "max": 5,
    "min": 0,
    "name": "level",
    "onlyInt": true,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
})
