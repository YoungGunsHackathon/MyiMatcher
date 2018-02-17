import numpy as np
from sklearn.manifold import TSNE
import json


class Matcher:
    ''' Class for matching people using autoencoder's latent space
    '''
    def edit_topics(self, arr):
        ''' Encode topic array to binary vector
        '''
        zeros = np.zeros(20)
        for x in range(len(arr)):
            index = arr[x]
            zeros[index] = 1
        return zeros

    def __init__(self, users):
        self.users = self.objects_from_json(users)
        for user in self.users:
            user.topics = self.edit_topics(user.topics)

    def objects_from_json(self, raw):
        ''' Function for creating objects from json
        '''
        js = raw.replace("\\", "")
        js = json.loads(js)
        attendants = []
        for x in range(len(js)):
            attendants.append(Attendant(js[x]['fname'], js[x]['lname'], js[x]['topics'], js[x]['career']))
        return attendants

    def test(self):
        X = []
        Y = []
        for user in self.users:
            X.append(np.array(user.topics))
            Y.append(user.fname + user.lname)
        X = np.array(X)
        Y = np.array(Y)
        np.save('X', X)
        np.save('Y', Y)
        return 'done bitch'



    def generate_training_set(self,X, Y):
        ''' Generate Training Set
        '''
        index = int(len(X) * 0.75)
        X_train = X[:index]
        X_test = X[index:]
        Y_train = Y[:index]
        Y_test = Y[index:]
        return X_train, X_test, Y_train, Y_test

    def sampling(self,args):
        z_mean, z_log_sigma = args
        epsilon = K.random_normal(shape=(batch_size, latent_dim),
                                  mean=0., std=epsilon_std)
        return z_mean + K.exp(z_log_sigma) * epsilon

    def generate_model(self,x_train, x_test, y_train, y_test):
        batch_size = 8
        original_dim = (x_train.shape[0] + x_test.shape[0], x_train.shape[1])
        latent_dim = (2, 1)
        intermediate_dim = (7, 1)
        x = Input(batch_shape=(batch_size, original_dim))
        h = Dense(intermediate_dim, activation='relu')(x)
        z_mean = Dense(latent_dim)(h)
        z_log_sigma = Dense(latent_dim)(h)



        z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_sigma])

        decoder_h = Dense(intermediate_dim, activation='relu')
        decoder_mean = Dense(original_dim, activation='sigmoid')
        h_decoded = decoder_h(z)
        x_decoded_mean = decoder_mean(h_decoded)

        # end-to-end autoencoder
        vae = Model(x, x_decoded_mean)

        # encoder, from inputs to latent space
        encoder = Model(x, z_mean)

        # generator, from latent space to reconstructed inputs
        decoder_input = Input(shape=(latent_dim,))
        _h_decoded = decoder_h(decoder_input)
        _x_decoded_mean = decoder_mean(_h_decoded)
        generator = Model(decoder_input, _x_decoded_mean)

        def vae_loss(x, x_decoded_mean):
            xent_loss = objectives.binary_crossentropy(x, x_decoded_mean)
            kl_loss = - 0.5 * K.mean(1 + z_log_sigma - K.square(z_mean) - K.exp(z_log_sigma), axis=-1)
            return xent_loss + kl_loss

        vae.compile(optimizer='rmsprop', loss=vae_loss)

        vae.fit(x_train, x_train,
            shuffle=True,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(x_test, x_test))

        return str(type(vae))

class Attendant:
    ''' Data class representing one event Attendant
    '''
    def __init__(self, fname, lname, topics, career):
        self.fname = fname
        self.lname = lname
        self.topics = topics
        self.career = career
