import pandas
import numpy
from matplotlib import pyplot as plt
import seaborn as sns


def plot_dataframe_corr(data : pandas.DataFrame) -> None:
    """Create correlation plot between numerical variables in a given dataframe.
    
    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame


    Returns
    -------
    None
        correlation plot
    
    """
    data_corr = data.corr(numeric_only=True)
    trimask = numpy.triu(data_corr)
    plt.figure(figsize=(10,7))
    sns.heatmap(data_corr, fmt = ".2f", square = True, annot= True, linewidths= .3, mask=trimask)
    plt.title('Correlation matrix')
    plt.tight_layout()
    plt.show()


def plot_target_corr(data : pandas.DataFrame, column: str) -> None:
    """Create correlation plot between numerical variables and target variable in a given dataframe.
    
    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame
    column : str
        target variable


    Returns
    -------
    None
        correlation plot with target variable
    
    """
    data_corr = data.corr(numeric_only=True)
    data_corr_y = data_corr[[column]].drop(column, axis=0).sort_values(by=column, ascending=False)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(t=f'Correlation with target: {column} \n', x=0.35, y=1)
    sns.heatmap(data_corr_y, fmt = ".2f", square = True, annot= True, linewidths= .3, ax=ax1)
    data.corr(numeric_only=True, method= "pearson")[column]\
    .drop(column, axis=0)\
    .sort_values(ascending=True)\
    .plot(figsize=(15,5), kind="barh", colormap='RdYlBu', ax=ax2)
    plt.tight_layout()
    plt.show()


def multiple_plots(data: pandas.DataFrame, columns: list, nrows: int, ncols: int, kind: str, target=None, target_labels=None, palette=None) -> None:
    """Create multiple plots in a grid.
    
    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame
    columns : list
        list of DataFrame columns
    nrows : int
        number of rows in the figure
    ncols : int
        number of columns in the figure
    kind : str
        'boxplot' or 'countplot' or 'histplot' or 'scatterplot'
    target : str
        target variable
    target_labels : list
        list of target labels
    palette : palette name, list, or dict
        colors to use for the different levels of the target variable


    Returns
    -------
    None
        multiple plots
    
    """             
    fig = plt.figure(figsize=((ncols*5), (nrows*5)))
    axes = fig.subplots(nrows=nrows, ncols=ncols)
    fig.subplots_adjust(hspace=0.4, wspace=0.2)
    for ax, column in zip(axes.flat, columns):
        if target == None:
            ax.set_title(f'{column} distribution')
        if target != None:
            ax.set_title(f'{column} distribution ~ {target}')
        if kind == 'boxplot' and target != None:
            sns.boxplot(y=data[column], ax=ax, color='steelblue', x=data[target], palette=palette)
            ax.set(xticklabels=target_labels)
        if kind == 'boxplot' and target == None:
            sns.boxplot(y=data[column], ax=ax, color='steelblue')
        if kind == 'countplot'and target == None:
            sns.countplot(x=data[column], ax=ax, palette=palette)
        if kind == 'countplot' and target != None:
            sns.countplot(x=data[column], ax=ax, hue=data[target], palette=palette)
        if kind == 'histplot':
            sns.histplot(x=data[column], kde=True, ax=ax, color='steelblue')
        if kind == 'scatterplot':
            sns.scatterplot(x=data[column], y=data[target], ax=ax, color='steelblue')
            ax.set_title(f"{target} ~ {column}")
    
    counter = 0
    counter += (nrows*ncols - len(columns))
    while counter > 0:
        axes.flat[-counter].axis('off')
        counter += -1
    plt.tight_layout()
    plt.show()
