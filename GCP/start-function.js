const Buffer = require('safe-buffer').Buffer;
const Compute = require('@google-cloud/compute');
const compute = new Compute();

/**
 * Starts a Compute Engine instance.
 *
 * Expects a PubSub message with JSON-formatted event data containing the
 * following attributes:
 *  zone - the GCP zone the instance is located in.
 *  instance - the name of the instance.
 *
 * @param {!object} event Cloud Function PubSub message event.
 * @param {!object} callback Cloud Function PubSub callback indicating completion.
 */
exports.startInstancePubSub = (event, callback) => {
  try {
    const pubsubMessage = event.data;
    const payload = _validatePayload(JSON.parse(Buffer.from(pubsubMessage.data, 'base64').toString()));
    compute.zone(payload.zone)
      .vm(payload.instance)
      .start()
      .then(data => {
        // Operation pending.
        const operation = data[0];
        return operation.promise();
      })
      .then(() => {
        // Operation complete. Instance successfully started.
        const message = 'Successfully started instance ' + payload.instance;
        console.log(message);
        callback(null, message);
      })
      .catch(err => {
        console.log(err);
        callback(err);
      });
  } catch (err) {
    console.log(err);
    callback(err);
  }
};

/**
 * Validates that a request payload contains the expected fields.
 *
 * @param {!object} payload the request payload to validate.
 * @returns {!object} the payload object.
 */
function _validatePayload (payload) {
  if (!payload.zone) {
    throw new Error(`Attribute 'zone' missing from payload`);
  } else if (!payload.instance) {
    throw new Error(`Attribute 'instance' missing from payload`);
  }
  return payload;
}