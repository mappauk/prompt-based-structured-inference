class EarlyStopping:
    def __init__(self, patience, required_metric_delta=0, greater_than_comparison=False):
        self.patience = patience
        self.required_metric_delta = required_metric_delta
        self.best_metric = None
        self.best_step = 0
        self.consecutive_epochs_without_improvement = 0
        self.training_flag = True
        self.greater_than_comparison = greater_than_comparison
    
    def check_early_stopping(self, current_metric_val, step):
        if self.best_metric == None or (self.greater_than_comparison and current_metric_val > (self.best_metric + self.required_metric_delta)) or (not self.greater_than_comparison and current_metric_val < (self.best_metric - self.required_metric_delta)):
            self.consecutive_epochs_without_improvement = 0
            self.best_metric = current_metric_val
            self.best_step = step
        elif self.consecutive_epochs_without_improvement + 1 >= self.patience:
            self.training_flag = False
            print(f'Validation Loss has not improved in {self.patience} epochs, the best performing epoch was {self.best_step}')
        else:
            self.consecutive_epochs_without_improvement += 1