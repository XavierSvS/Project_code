    def PoluteSignal(CleanSignals, delta=0.10):
        #CleanSignals is (s x n):
        #   n are the timesteps, s are the dofs
        #   delta is the Noise Percentage, e.g. 10% noise is 0.10

        CleanSignals = CleanSignals.T

        mean = np.mean(CleanSignals, axis=0)
        std = np.sqrt(np.sum((CleanSignals-mean)**2/CleanSignals.shape[0], axis=0))

        noisy_signal=CleanSignals+delta*std*np.random.normal(size=CleanSignals.shape)
        noisy_signal=noisy_signal.squeeze()

        return noisy_signal.T
