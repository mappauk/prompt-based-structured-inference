class EarlyStopping:
    def __init__(self, patience, required_loss_delta=0):
        self.patience = patience
        self.required_loss_delta = required_loss_delta
        self.lowest_loss = None
        self.best_epoch = 0
        self.consecutive_epochs_without_improvement = 0
        self.training_flag = True
    
    def check_early_stopping(self, val_loss, epoch):
        if self.lowest_loss == None or (val_loss < (self.lowest_loss - self.required_loss_delta)):
            self.consecutive_epochs_without_improvement = 0
            self.lowest_loss = val_loss
            self.best_epoch = epoch
        elif self.consecutive_epochs_without_improvement + 1 >= self.patience:
            self.training_flag = False
            print(f'Validation Loss has not improved in {self.patience} epochs, the best performing epoch was {self.best_epoch}')
        else:
            self.consecutive_epochs_without_improvement += 1